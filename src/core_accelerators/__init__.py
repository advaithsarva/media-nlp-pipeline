"""Python package wrapping the compiled `_core_accelerators` pybind11 extension.

Just a re-export. The extension itself is built from text_ops.cpp/nlp_accel.cpp via
CMakeLists.txt in this directory and is not part of the default install, so importing
this package must succeed even on a checkout where nothing has been compiled --
`nlp_pipeline.native_accel` is what actually decides, via `NATIVE_BUILT` below, whether
to use the compiled path or its pure-Python fallback.
"""

try:
    from ._core_accelerators import count_lexicon_hits, count_ngrams, is_punct, tokenize
    NATIVE_BUILT = True
except ImportError:
    NATIVE_BUILT = False

__all__ = ["NATIVE_BUILT", "tokenize", "is_punct", "count_ngrams", "count_lexicon_hits"]
