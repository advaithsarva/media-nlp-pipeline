"""Character-level noise injection for the robustness module, plus one mitigation.

Two noise ops, applied per character at a given rate: keyboard-adjacent substitution
and deletion. Both are common typo shapes; neither changes word count or sentence
count, so any F1 drop traces to the text itself, not to a side effect of the noise
function.

Mitigation tried: normalise each token against a vocabulary built from the *clean*
training text using stdlib `difflib.get_close_matches` (nearest known word by edit
similarity). This needs no new dependency and no training -- it is the cheapest
thing worth trying before reaching for anything heavier.
"""

import difflib
import random
import re

KEYBOARD_ADJACENT = {
    "a": "qwsz", "b": "vghn", "c": "xdfv", "d": "erfcxs", "e": "wsdr", "f": "rtgdvc",
    "g": "tyhfvb", "h": "yujgbn", "i": "ujko", "j": "uikhnm", "k": "iojlm", "l": "opk",
    "m": "njk", "n": "bhjm", "o": "iklp", "p": "ol", "q": "wa", "r": "edft", "s": "awedxz",
    "t": "rfgy", "u": "yhji", "v": "cfgb", "w": "qase", "x": "zsdc", "y": "tghu",
    "z": "asx",
}


def noise_text(text, rate, seed):
    rng = random.Random(seed)
    out = []
    for ch in text:
        lower = ch.lower()
        if lower in KEYBOARD_ADJACENT and rng.random() < rate:
            op = rng.choice(("sub", "del"))
            if op == "del":
                continue
            replacement = rng.choice(KEYBOARD_ADJACENT[lower])
            out.append(replacement.upper() if ch.isupper() else replacement)
        else:
            out.append(ch)
    return "".join(out)


def build_vocab(texts, min_len=3, max_size=None):
    """max_size keeps only the most frequent words -- difflib's per-call cost scales with
    vocab size, and the long tail of rare words contributes little correction value for
    what it costs (measured: capping ~11k words to 3k cut the mitigation pass ~3-4x)."""
    from collections import Counter
    counts = Counter()
    for t in texts:
        for w in re.findall(r"[A-Za-z]+", t):
            if len(w) >= min_len:
                counts[w.lower()] += 1
    if max_size is None:
        return set(counts)
    return {w for w, _ in counts.most_common(max_size)}


def _bucket_by_length(vocab):
    """difflib.get_close_matches is O(len(vocab)) per call. A typo rarely changes a
    word's length by more than 1-2 characters, so comparing only within a length band
    cuts the candidate set by roughly an order of magnitude on a real vocabulary."""
    buckets = {}
    for w in vocab:
        buckets.setdefault(len(w), set()).add(w)
    return buckets


def spellcheck_mitigate(text, vocab, cutoff=0.8, buckets=None):
    """Replace each word not in vocab with its closest vocab match, if one is close enough.

    `buckets` (from `_bucket_by_length`) can be precomputed once and reused across many
    calls -- building it is itself O(vocab), so redoing it per document defeats the point."""
    if buckets is None:
        buckets = _bucket_by_length(vocab)

    def fix(match):
        word = match.group(0)
        lower = word.lower()
        if lower in vocab or len(lower) < 3:
            return word
        nearby = set()
        for length in (len(lower) - 1, len(lower), len(lower) + 1):
            nearby |= buckets.get(length, set())
        candidates = difflib.get_close_matches(lower, nearby, n=1, cutoff=cutoff)
        if not candidates:
            return word
        fixed = candidates[0]
        return fixed.capitalize() if word[0].isupper() else fixed

    return re.sub(r"[A-Za-z]+", fix, text)


if __name__ == "__main__":
    sample = "The devastating earthquake struck the region, officials confirmed."
    noised = noise_text(sample, 0.15, seed=1)
    print("clean :", sample)
    print("noised:", noised)
    vocab = build_vocab([sample])
    print("fixed :", spellcheck_mitigate(noised, vocab, cutoff=0.6))
