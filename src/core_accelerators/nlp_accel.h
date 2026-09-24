// Higher-level NLP acceleration -- the document-level loops that get slow on large
// documents, as opposed to text_ops.h's single-pass character scanning.
#pragma once

#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

namespace core_accelerators {

// Sliding-window n-gram counts over `words` (already-lowercased token strings, exactly
// what `rules_engine.RuleEngine._scan_repetition` builds from `Token.lower`). The n-gram
// key is its words joined with a single space, matching the Python side's
// `" ".join(w.lower for w in group)` exactly -- this is what lets `RuleEngine` swap its
// `collections.Counter` call for this function with no change in the phrases it flags.
//
// Iteration order of the returned map is not meaningful (hash map); callers that need a
// stable order -- `RuleEngine` does -- sort afterwards, exactly as the Python
// `collections.Counter` path already required doing.
std::unordered_map<std::string, int> count_ngrams(const std::vector<std::string>& words, int n);

// How many of `words` appear in `lexicon` -- the token-level membership test underlying
// a lexicon detector, accelerated for documents where the term list is large.
int count_lexicon_hits(const std::vector<std::string>& words,
                       const std::unordered_set<std::string>& lexicon);

}  // namespace core_accelerators
