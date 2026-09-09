r"""Optional native acceleration for the hottest loops in `preprocessing.py` and
`rules_engine.py`, backed by the pybind11 extension in `src/core_accelerators/`.

Nothing in the pipeline requires this module's native path. `core_accelerators` is built
by hand (see `src/core_accelerators/CMakeLists.txt`) and is not part of the default
install, so every function here falls back to a pure-Python implementation when the
compiled extension is not importable. `NATIVE_AVAILABLE` says which path is active.

The rule this module is built around: the native and fallback `tokenize()` implementations
agree on every realistic input -- ASCII, accented Latin, CJK, Cyrillic, Greek, emoji,
common punctuation -- which `tests/test_native_accel.py`'s fuzz test checks directly.
They are documented, not silently assumed, to diverge on one narrow, rare class of input:
`text_ops.cpp`'s file comment records that Python's Unicode-database-driven `\w` counts a
few extra number-like categories (Roman numeral symbols, circled digits, superscripts,
vulgar fractions) as word characters that glibc's locale-based `iswalnum` does not. That
is exactly why `tokenize()` here is offered as an available, independently-tested
accelerator rather than swapped into `preprocessing.TextProcessor._tokenize` itself --
the character offsets every finding's evidence span is checked against
(`postprocessing.check_evidence`) keep coming from the Python regex tokenizer.
"""

import re
from collections import Counter
from typing import Dict, Iterable, List, Tuple

try:
    import core_accelerators as _native
    NATIVE_AVAILABLE = bool(getattr(_native, "NATIVE_BUILT", False))
except ImportError:
    _native = None
    NATIVE_AVAILABLE = False


# Kept identical to preprocessing.TOKEN_PATTERN on purpose: this *is* the reference
# implementation tokenize() must agree with, native or not.
_TOKEN_PATTERN = re.compile(r"\w+(?:['’]\w+)*|[^\w\s]")


def _tokenize_python(text: str) -> List[Tuple[str, int]]:
    return [(m.group(), m.start()) for m in _TOKEN_PATTERN.finditer(text)]


def tokenize(text: str) -> List[Tuple[str, int]]:
    """`[(token_text, start_idx), ...]`, exactly what `TextProcessor._tokenize` derives
    `Token.text`/`Token.idx` from -- see that class for turning this into full `Token`s."""
    if NATIVE_AVAILABLE:
        return _native.tokenize(text)
    return _tokenize_python(text)


def is_punct(word: str) -> bool:
    if NATIVE_AVAILABLE:
        return _native.is_punct(word)
    return all(not ch.isalnum() for ch in word)


def _count_ngrams_python(words: List[str], n: int) -> Dict[str, int]:
    if n <= 0 or len(words) < n:
        return {}
    counts = Counter(" ".join(words[i:i + n]) for i in range(len(words) - n + 1))
    return dict(counts)


def count_ngrams(words: Iterable[str], n: int) -> Dict[str, int]:
    """Sliding-window n-gram counts, phrase -> count. Matches the `collections.Counter`
    step in `RuleEngine._scan_repetition`, just without building a `Counter` object --
    callers that want one can wrap the result in `Counter(...)`."""
    words = list(words)
    if NATIVE_AVAILABLE:
        return _native.count_ngrams(words, n)
    return _count_ngrams_python(words, n)


def count_lexicon_hits(words: Iterable[str], lexicon: Iterable[str]) -> int:
    words = list(words)
    lexicon_set = set(lexicon)
    if NATIVE_AVAILABLE:
        return _native.count_lexicon_hits(words, list(lexicon_set))
    return sum(1 for w in words if w in lexicon_set)
