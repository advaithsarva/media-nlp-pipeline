// Heavy text ops that stay bit-identical to their Python originals -- see text_ops.cpp
// for why exactness, not just speed, is the point of this module.
#pragma once

#include <cstddef>
#include <string>
#include <utility>
#include <vector>

namespace core_accelerators {

// One token: its exact text and the UTF-32 codepoint offset it starts at in the source
// string. Matches `nlp_pipeline.preprocessing.TextProcessor._tokenize`'s notion of a
// token, minus the stopword/lemma labels, which are simple lookups the Python side
// already does cheaply.
struct TokenSpan {
    std::string text;
    std::size_t idx;
};

// Prefix-scans `text` (an NFC-normalised, UTF-8 encoded string) into the same tokens
// `preprocessing.TOKEN_PATTERN` (`r"\w+(?:['’]\w+)*|[^\w\s]"`) would produce: a run
// of word characters, optionally continued past an apostrophe by more word characters
// (so "don't" is one token), or a single non-space, non-word symbol.
//
// Offsets are codepoint indices, not byte indices, matching Python's `str` indexing --
// this is the reason the function is not a plain byte-level `for` loop despite the UTF-8
// input.
std::vector<TokenSpan> tokenize(const std::string& text);

// True when every character in `word` is neither alphanumeric nor an underscore --
// i.e. what `TextProcessor._is_punct` computes for a token's own text.
bool is_punct(const std::string& word);

}  // namespace core_accelerators
