"""native_accel's contract: the compiled extension (when built) and its pure-Python
fallback must agree, always. The fuzz test is what actually earns trust in the C++
tokenizer's Unicode handling; the fixed-example tests exist so a failure is readable at
a glance instead of only as a fuzzed string.

`TestNativeExtension` below skips itself when src/core_accelerators has not been
compiled -- building it is optional (see CMakeLists.txt in that directory), and CI/dev
environments that never ran `cmake --build` should not fail this suite for a component
the rest of the pipeline does not require. `test_dispatch_*` at module level is not
skipped: `nlp_pipeline.native_accel`'s public functions must be correct on the
pure-Python fallback too, since that is what every environment without a C++ toolchain
actually runs.
"""

import random
import re

import pytest

from nlp_pipeline import native_accel as na

# The exact regex tokenize() must agree with -- see preprocessing.TOKEN_PATTERN.
_TOKEN_PATTERN = re.compile(r"\w+(?:['’]\w+)*|[^\w\s]")


def test_dispatch_tokenize_matches_python_regex():
    text = "The plan was disastrous, and it's not what we expected."
    expected = [(m.group(), m.start()) for m in _TOKEN_PATTERN.finditer(text)]
    assert na.tokenize(text) == expected


def test_dispatch_is_punct():
    assert na.is_punct("...") is True
    assert na.is_punct("word") is False


def test_dispatch_count_ngrams():
    words = ["a", "b", "a", "b", "c"]
    assert na.count_ngrams(words, 2) == {"a b": 2, "b a": 1, "b c": 1}


def test_dispatch_count_lexicon_hits():
    words = ["a", "b", "a", "b", "c"]
    assert na.count_lexicon_hits(words, ["a", "c"]) == 3


def test_dispatch_matches_whichever_backend_is_active():
    """Whether NATIVE_AVAILABLE is True or False, the dispatching wrapper must return
    exactly what that active backend computes -- no silent divergence between them."""
    text = "Café naïve, don’t you think?"
    reference = na._native.tokenize(text) if na.NATIVE_AVAILABLE else na._tokenize_python(text)
    assert na.tokenize(text) == reference


FIXED_EXAMPLES = [
    "The quick brown fox jumps over the lazy dog.",
    "She said, \"It’s a don’t-care situation—really!\" (allegedly)",
    "Café naïve résumé Zürich Москва 東京 Ελλάδα coöperate",
    "Multiple   spaces\tand\nnewlines\r\nhere.",
    "",
    "   ",
    "word’s ‘quoted’ “curly” text… 100% £©®",
    "emoji test \U0001F600 done",
    "_ __init__ a_b CamelCase123 5.5 中文",
]


@pytest.mark.skipif(
    not na.NATIVE_AVAILABLE,
    reason="core_accelerators extension not built (see src/core_accelerators/CMakeLists.txt)",
)
class TestNativeExtension:
    """Everything here talks to the compiled `_core_accelerators` extension directly,
    so it only makes sense to run where that extension was actually built."""

    @pytest.mark.parametrize("text", FIXED_EXAMPLES)
    def test_tokenize_matches_python_regex(self, text):
        expected = [(m.group(), m.start()) for m in _TOKEN_PATTERN.finditer(text)]
        assert na._native.tokenize(text) == expected

    @pytest.mark.parametrize("word", ["hello", "...", "_", "5", "", "a1", "!!!", "don't", "’", "__init__"])
    def test_is_punct_matches_python(self, word):
        expected = all(not ch.isalnum() for ch in word)
        assert na._native.is_punct(word) == expected

    def test_count_ngrams_matches_python_counter(self):
        words = ["we", "will", "take", "back", "control", "we", "will", "take", "back", "control", "again"]
        for n in (1, 2, 3, 4):
            assert na._native.count_ngrams(words, n) == na._count_ngrams_python(words, n)

    def test_count_lexicon_hits_matches_python(self):
        words = ["disastrous", "shameful", "the", "plan", "disastrous"]
        lexicon = ["disastrous", "shameful"]
        expected = sum(1 for w in words if w in set(lexicon))
        assert na._native.count_lexicon_hits(words, lexicon) == expected

    def test_fuzz_tokenize_agrees_with_python_regex(self):
        rng = random.Random(1234)
        pool = list("abcABC123 \t\n.,!?'’\"“”—–…") + ["café", "日本語", "Ω", "_", "__", "\U0001F600"]

        mismatches = []
        for _ in range(500):
            text = "".join(rng.choice(pool) for _ in range(rng.randint(0, 60)))
            expected = [(m.group(), m.start()) for m in _TOKEN_PATTERN.finditer(text)]
            actual = na._native.tokenize(text)
            if expected != actual:
                mismatches.append((text, expected, actual))

        assert not mismatches, mismatches[:3]
