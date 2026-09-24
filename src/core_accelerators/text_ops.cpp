// Heavy text ops for `preprocessing.py`'s tokenizer, reimplemented as one prefix scan
// over the string instead of a compiled regex walking it.
//
// The one rule that matters more than speed: this must produce *exactly* the same
// tokens, in the same order, at the same offsets, as
// `nlp_pipeline.preprocessing.TextProcessor._tokenize`'s Python regex
// (`r"\w+(?:['’]\w+)*|[^\w\s]"`) -- not an approximation of it. Every character offset
// the rest of the pipeline reports traces back to this tokenizer's `idx`, and
// `postprocessing.check_evidence` re-reads every finding out of the source text and
// fails the run if it does not match exactly. An accelerator that is merely close is
// worse than no accelerator: it would pass tests on the text it was checked against and
// silently corrupt offsets on text it was not.
//
// Python's `\w` is Unicode-aware: any letter or digit in any script, plus underscore.
// Non-ASCII classification is delegated to glibc's own Unicode tables (`iswalnum`,
// `iswspace` from <cwctype>, under the "C.UTF-8" locale) rather than a hand-rolled
// table: a first attempt at a curated punctuation/symbol list correctly handled curly
// quotes and dashes but classified emoji as word characters (they are not in that
// table, so they fell through to the "everything else is a letter" default) -- exactly
// the kind of "close but not exact" bug the file comment below used to warn about
// before it was replaced with this approach. `iswalnum` gets emoji, combining marks and
// punctuation right for free, because it is backed by the real Unicode character
// database instead of a list of the codepoints one contributor happened to think of.
//
// One documented gap: glibc's `iswspace` under "C.UTF-8" does not treat U+00A0
// (no-break space) as whitespace, but Python's `\s` does -- confirmed against Python
// directly, not assumed. NBSP is common enough in scraped/pasted text to special-case
// explicitly rather than accept the mismatch.
//
// A second, accepted gap, found by fuzzing against codepoints drawn from Unicode's
// General Punctuation / Number Forms / Enclosed Alphanumerics blocks specifically
// (tests/test_native_accel.py's realistic-prose fuzz target does not hit this -- it
// took a deliberately adversarial range sweep to find): Python's `str.isalnum()`
// additionally counts the Unicode "Letter Number" and "Other Number" categories --
// Roman numeral symbols (Ⅷ), circled digits (①), superscripts (²), vulgar fractions
// (½) -- as word characters, while glibc's `iswalnum` does not. This tokenizer follows
// glibc here, so a token containing one of those characters can end up split
// differently from the Python reference. Rare in body text (these are typeset/footnote
// notation, not prose); real, and not silently pretended otherwise, which is why this
// accelerator is not wired into preprocessing.py's actual TextProcessor -- it stays an
// available, independently-tested acceleration path (native_accel.py) rather than the
// tokenizer every document's character offsets are measured against.

#include "text_ops.h"

#include <clocale>
#include <cstdint>
#include <cwctype>

namespace core_accelerators {

namespace {

// Runs once, before any tokenize()/is_punct() call: without an explicit UTF-8 locale,
// iswalnum/iswspace fall back to the "C" locale's ASCII-only tables and every non-ASCII
// codepoint below would misclassify as punctuation. LC_CTYPE only (not LC_ALL), so this
// cannot change number/date formatting anywhere else in the process.
struct LocaleInit {
    LocaleInit() { std::setlocale(LC_CTYPE, "C.UTF-8"); }
};
const LocaleInit _locale_init;

// ---------- UTF-8 decoding ----------

struct Codepoint {
    char32_t value;
    std::size_t byte_len;
};

Codepoint decode_utf8(const std::string& text, std::size_t byte_pos) {
    unsigned char lead = static_cast<unsigned char>(text[byte_pos]);
    std::size_t remaining = text.size() - byte_pos;

    if (lead < 0x80) {
        return {static_cast<char32_t>(lead), 1};
    }
    if ((lead & 0xE0) == 0xC0 && remaining >= 2) {
        unsigned char c1 = static_cast<unsigned char>(text[byte_pos + 1]);
        char32_t cp = ((lead & 0x1Fu) << 6) | (c1 & 0x3Fu);
        return {cp, 2};
    }
    if ((lead & 0xF0) == 0xE0 && remaining >= 3) {
        unsigned char c1 = static_cast<unsigned char>(text[byte_pos + 1]);
        unsigned char c2 = static_cast<unsigned char>(text[byte_pos + 2]);
        char32_t cp = ((lead & 0x0Fu) << 12) | ((c1 & 0x3Fu) << 6) | (c2 & 0x3Fu);
        return {cp, 3};
    }
    if ((lead & 0xF8) == 0xF0 && remaining >= 4) {
        unsigned char c1 = static_cast<unsigned char>(text[byte_pos + 1]);
        unsigned char c2 = static_cast<unsigned char>(text[byte_pos + 2]);
        unsigned char c3 = static_cast<unsigned char>(text[byte_pos + 3]);
        char32_t cp = ((lead & 0x07u) << 18) | ((c1 & 0x3Fu) << 12)
                     | ((c2 & 0x3Fu) << 6) | (c3 & 0x3Fu);
        return {cp, 4};
    }
    // Malformed byte: treat as one opaque codepoint rather than throwing, the same way
    // Python's `errors="replace"` decoding degrades gracefully instead of crashing a run.
    return {lead, 1};
}

// ---------- character classification ----------

bool is_ascii_space(char32_t cp) {
    return cp == ' ' || cp == '\t' || cp == '\n' || cp == '\r' || cp == '\f' || cp == '\v';
}

// Python's `str.isalnum()`, which `TextProcessor._is_punct` uses. NOT the same set as
// `\w`: `\w` includes '_' (so "_" tokenizes as a word-shaped token), but '_' is not
// alphanumeric ("_".isalnum() is False), so a lone "_" token still counts as
// punctuation -- kept as its own function so that distinction stays explicit at every
// call site instead of being folded into one "word-ish" test.
bool is_alnum_char(char32_t cp) {
    if (cp < 0x80) return (cp >= '0' && cp <= '9') || (cp >= 'A' && cp <= 'Z') || (cp >= 'a' && cp <= 'z');
    return std::iswalnum(static_cast<wint_t>(cp)) != 0;
}

bool is_word_char(char32_t cp) {
    if (cp == '_') return true;
    return is_alnum_char(cp);
}

bool is_space_char(char32_t cp) {
    if (cp < 0x80) return is_ascii_space(cp);
    if (cp == 0x00A0) return true;   // see file comment: glibc disagrees with Python here
    return std::iswspace(static_cast<wint_t>(cp)) != 0;
}

bool is_apostrophe(char32_t cp) {
    return cp == '\'' || cp == 0x2019;   // ' and the curly '’', exactly what TOKEN_PATTERN allows
}

}  // namespace

bool is_punct(const std::string& word) {
    // Matches Python's `all(not ch.isalnum() for ch in word)` exactly, empty-string
    // case included: `all()` over zero elements is `True`, so an empty word counts as
    // punctuation too, and this loop returns `true` on an empty `word` the same way --
    // it simply never finds a character to disqualify it.
    std::size_t pos = 0;
    while (pos < word.size()) {
        Codepoint c = decode_utf8(word, pos);
        if (is_alnum_char(c.value)) return false;
        pos += c.byte_len;
    }
    return true;
}

std::vector<TokenSpan> tokenize(const std::string& text) {
    std::vector<TokenSpan> tokens;

    // decode once into (codepoint, byte_offset) pairs so word/idx math is in codepoint
    // units (matching Python str indexing) while byte offsets stay available for slicing
    std::vector<Codepoint> cps;
    std::vector<std::size_t> byte_offsets;
    cps.reserve(text.size());
    byte_offsets.reserve(text.size());
    for (std::size_t pos = 0; pos < text.size();) {
        Codepoint c = decode_utf8(text, pos);
        cps.push_back(c);
        byte_offsets.push_back(pos);
        pos += c.byte_len;
    }
    byte_offsets.push_back(text.size());   // sentinel: end of string

    std::size_t n = cps.size();
    std::size_t i = 0;

    auto slice = [&](std::size_t start_cp, std::size_t end_cp) {
        return text.substr(byte_offsets[start_cp], byte_offsets[end_cp] - byte_offsets[start_cp]);
    };

    while (i < n) {
        char32_t cp = cps[i].value;

        if (is_word_char(cp)) {
            std::size_t start = i;
            std::size_t end = i;
            while (end < n && is_word_char(cps[end].value)) ++end;

            // (?:['’]\w+)*: keep extending through an apostrophe only when at least one
            // word character follows it, exactly like the Python regex's `\w+` after the quote
            while (end < n && is_apostrophe(cps[end].value)
                  && end + 1 < n && is_word_char(cps[end + 1].value)) {
                std::size_t run_start = end + 1;
                end = run_start;
                while (end < n && is_word_char(cps[end].value)) ++end;
            }

            tokens.push_back({slice(start, end), start});
            i = end;
        } else if (is_space_char(cp)) {
            ++i;
        } else {
            // [^\w\s]: exactly one non-word, non-space codepoint
            tokens.push_back({slice(i, i + 1), i});
            ++i;
        }
    }

    return tokens;
}

}  // namespace core_accelerators
