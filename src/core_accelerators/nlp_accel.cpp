// See nlp_accel.h. Both functions here are pure counting -- no text classification, so
// unlike text_ops.cpp there is no Unicode edge case to get subtly wrong; correctness is
// just "does the same arithmetic as the Python loop it replaces".

#include "nlp_accel.h"

#include <sstream>

namespace core_accelerators {

std::unordered_map<std::string, int> count_ngrams(const std::vector<std::string>& words, int n) {
    std::unordered_map<std::string, int> counts;
    if (n <= 0 || static_cast<int>(words.size()) < n) {
        return counts;
    }

    // Reused buffer, joined incrementally window-to-window rather than rebuilt from
    // scratch: rules_engine.py's whole reason for wanting this accelerated is that a
    // long document turns "build every n-gram string" into the dominant cost.
    for (std::size_t i = 0; i + static_cast<std::size_t>(n) <= words.size(); ++i) {
        std::string key;
        std::size_t total_len = 0;
        for (int j = 0; j < n; ++j) total_len += words[i + j].size() + 1;
        key.reserve(total_len);

        for (int j = 0; j < n; ++j) {
            if (j > 0) key.push_back(' ');
            key += words[i + j];
        }
        ++counts[key];
    }
    return counts;
}

int count_lexicon_hits(const std::vector<std::string>& words,
                       const std::unordered_set<std::string>& lexicon) {
    int hits = 0;
    for (const auto& word : words) {
        if (lexicon.find(word) != lexicon.end()) ++hits;
    }
    return hits;
}

}  // namespace core_accelerators
