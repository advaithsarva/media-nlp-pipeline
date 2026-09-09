// PyBind11 bridge -> the `core_accelerators` Python extension module.
//
// Every function here is a pure function over plain Python types (str, list[str], int)
// in, plain Python types out -- no custom types cross the boundary, so the extension has
// no lifetime/ownership questions to get wrong, and `native_accel.py`'s pure-Python
// fallback can mirror each signature exactly.

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "nlp_accel.h"
#include "text_ops.h"

namespace py = pybind11;

PYBIND11_MODULE(_core_accelerators, m) {
    m.doc() = "C++ CPU acceleration for the hottest text-processing loops in "
              "nlp_pipeline (see src/core_accelerators/*.cpp for the Python "
              "equivalent each function must stay bit-identical to).";

    m.def(
        "tokenize",
        [](const std::string& text) {
            std::vector<core_accelerators::TokenSpan> spans = core_accelerators::tokenize(text);
            std::vector<std::pair<std::string, std::size_t>> out;
            out.reserve(spans.size());
            for (const auto& s : spans) out.emplace_back(s.text, s.idx);
            return out;
        },
        py::arg("text"),
        "Tokenize `text` into [(token_text, codepoint_start_idx), ...], matching "
        "preprocessing.TextProcessor._tokenize's TOKEN_PATTERN regex exactly."
    );

    m.def("is_punct", &core_accelerators::is_punct, py::arg("word"),
         "True when every character in `word` is neither alphanumeric nor '_'.");

    m.def(
        "count_ngrams",
        [](const std::vector<std::string>& words, int n) {
            return core_accelerators::count_ngrams(words, n);
        },
        py::arg("words"), py::arg("n"),
        "Sliding-window n-gram counts over already-lowercased `words`, keyed by "
        "space-joined phrase -- accelerates RuleEngine._scan_repetition's Counter step."
    );

    m.def(
        "count_lexicon_hits",
        [](const std::vector<std::string>& words, const std::vector<std::string>& lexicon) {
            std::unordered_set<std::string> lexicon_set(lexicon.begin(), lexicon.end());
            return core_accelerators::count_lexicon_hits(words, lexicon_set);
        },
        py::arg("words"), py::arg("lexicon"),
        "How many of `words` appear in `lexicon`."
    );
}
