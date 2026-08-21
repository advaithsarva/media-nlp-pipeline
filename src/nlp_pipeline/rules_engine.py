"""Runs the taxonomy's detectors over the text and returns evidence spans.

Two properties matter more than coverage here:

1. Every hit carries the exact substring plus its start and end position in the original
   document, so a reader can check the claim against the article. Nothing is paraphrased.
2. The same document always produces the same spans in the same order. Categories,
   sentences and patterns are all walked in a fixed order, and the result is sorted before
   it is returned.

Five detector kinds, each matching a rule shape that actually appears in the design notes:

    lexicon        a word from a list                       "disastrous"
    regex          a phrase pattern                         "everyone knows"
    regex_unless   a pattern, but only when the sentence     "many people" with no
                   does NOT also contain a context cue       number, %, study or source
    cooccurrence   N or more terms from a list inside one    two virtue words in a
                   short sentence                            slogan-length sentence
    repetition     an n-gram repeated across the document    a slogan used four times

`regex_unless` is the one that makes precision possible. "Many respondents (37%) agreed"
and "many people are saying" are the same phrase doing opposite jobs; only the presence of
supporting context separates them.
"""

import re
from collections import Counter

from nlp_pipeline.shared_types import EvidenceSpan, RuleClassificationResult, NormalizedDocument

DETECTOR_KINDS = ("lexicon", "regex", "regex_unless", "cooccurrence", "repetition")


class RuleEngine:
    def __init__(self, taxonomy, threshold=None):
        self.taxonomy = taxonomy
        self.threshold = taxonomy.default_threshold if threshold is None else threshold
        self.rules = self._compile_rules()

    # ---------- setup ----------

    def _lexicon_pattern(self, terms):
        """One alternation regex for a whole word list, so the text is scanned once.

        re.escape matters: nothing in the current lists contains a regex-special
        character, but a term added later with a "." or "(" would quietly break the
        pattern rather than fail.
        """
        return re.compile(r"\b(?:" + "|".join(re.escape(t) for t in terms) + r")\b", re.IGNORECASE)

    def _compile_rules(self):
        compiled = []
        for cat in self.taxonomy.categories:
            if cat.detector == "lexicon":
                compiled.append({
                    "category": cat,
                    "rule_id": cat.id + ":lexicon",
                    "kind": "lexicon",
                    "pattern": self._lexicon_pattern(cat.terms),
                })

            elif cat.detector == "regex":
                for i, pattern in enumerate(cat.patterns):
                    compiled.append({
                        "category": cat,
                        "rule_id": cat.id + ":regex:" + str(i),
                        "kind": "regex",
                        "pattern": re.compile(pattern, re.IGNORECASE),
                    })

            elif cat.detector == "regex_unless":
                # one shared "the sentence is properly supported" test for the category
                unless = self._lexicon_pattern(cat.unless_terms) if cat.unless_terms else None
                unless_patterns = [re.compile(p, re.IGNORECASE) for p in cat.unless_patterns]
                for i, pattern in enumerate(cat.patterns):
                    compiled.append({
                        "category": cat,
                        "rule_id": cat.id + ":unless:" + str(i),
                        "kind": "regex_unless",
                        "pattern": re.compile(pattern, re.IGNORECASE),
                        "unless": unless,
                        "unless_patterns": unless_patterns,
                    })

            elif cat.detector == "cooccurrence":
                compiled.append({
                    "category": cat,
                    "rule_id": cat.id + ":cooccurrence",
                    "kind": "cooccurrence",
                    "pattern": self._lexicon_pattern(cat.terms),
                    "min_hits": cat.min_hits,
                    "max_words": cat.max_words,
                })

            elif cat.detector == "repetition":
                compiled.append({
                    "category": cat,
                    "rule_id": cat.id + ":repetition",
                    "kind": "repetition",
                    "ngram_size": cat.ngram_size,
                    "min_repeats": cat.min_repeats,
                })

            else:
                raise ValueError(cat.id + ": unknown detector " + repr(cat.detector))

        return compiled

    # ---------- the detectors ----------

    def _span(self, doc, sentence, start, end, rule, confidence=None):
        cat = rule["category"]
        return EvidenceSpan(
            text=doc.text[start:end],
            start_char=start,
            end_char=end,
            rule_id=rule["rule_id"],
            category=cat.id,
            confidence=cat.base_confidence if confidence is None else confidence,
            sentence_id=sentence.sentence_id,
        )

    def _is_supported(self, sentence_text, rule):
        """True when the sentence carries the evidence that makes the phrase legitimate.

        "Many (37%) of respondents" is supported. "Many people say" is not.
        """
        if rule["unless"] is not None and rule["unless"].search(sentence_text):
            return True
        for pattern in rule["unless_patterns"]:
            if pattern.search(sentence_text):
                return True
        return False

    def _scan_sentence(self, doc, sentence, rule):
        kind = rule["kind"]
        text = sentence.text
        offset = sentence.start_char
        found = []

        if kind in ("lexicon", "regex"):
            for match in rule["pattern"].finditer(text):
                found.append(self._span(doc, sentence, offset + match.start(),
                                        offset + match.end(), rule))

        elif kind == "regex_unless":
            if not self._is_supported(text, rule):
                for match in rule["pattern"].finditer(text):
                    found.append(self._span(doc, sentence, offset + match.start(),
                                            offset + match.end(), rule))

        elif kind == "cooccurrence":
            matches = list(rule["pattern"].finditer(text))
            # a slogan is short and dense; the same two words spread across a long
            # explanatory sentence is ordinary writing, not a slogan
            word_count = len(text.split())
            if len(matches) >= rule["min_hits"] and word_count <= rule["max_words"]:
                # one span covering first hit to last, so the evidence shows the pairing
                start = offset + matches[0].start()
                end = offset + matches[-1].end()
                found.append(self._span(doc, sentence, start, end, rule))

        return found

    def _scan_repetition(self, doc, rule):
        """Phrases repeated across the whole document -- a document-level detector.

        Unlike the others this cannot work sentence by sentence, because the signal is
        precisely that the same phrase keeps coming back.
        """
        size = rule["ngram_size"]
        words = [t for t in doc.tokens if not t.is_punct]
        if len(words) < size:
            return []

        # build every n-gram with the position it starts at, so evidence stays quotable
        ngrams = []
        for i in range(len(words) - size + 1):
            group = words[i:i + size]
            # "of the people in" repeats in any long document and means nothing. A phrase
            # only counts as deliberate repetition if it carries at least one real word.
            if all(w.is_stop for w in group):
                continue
            phrase = " ".join(w.lower for w in group)
            start = group[0].idx
            end = group[-1].idx + len(group[-1].text)
            ngrams.append((phrase, start, end))

        counts = Counter(phrase for phrase, _, _ in ngrams)
        found = []
        last_end = -1
        for phrase, start, end in ngrams:
            if counts[phrase] < rule["min_repeats"]:
                continue
            # The window slides one word at a time, so a four-word repeated slogan matches
            # as several overlapping n-grams. Reporting all of them turns one repetition
            # into five findings. Keep the first and skip anything overlapping it, which
            # leaves exactly one span per actual occurrence.
            if start < last_end:
                continue
            sentence = self._sentence_at(doc, start)
            if sentence is None:
                continue
            found.append(self._span(doc, sentence, start, end, rule))
            last_end = end
        return found

    def _sentence_at(self, doc, position):
        for sentence in doc.sentences:
            if sentence.start_char <= position < sentence.end_char:
                return sentence
        return None

    # ---------- entry point ----------

    def classify(self, doc: NormalizedDocument) -> RuleClassificationResult:
        spans = []

        for rule in self.rules:
            if rule["category"].base_confidence < self.threshold:
                continue    # the R2 gate: a detector below threshold never emits

            if rule["kind"] == "repetition":
                spans.extend(self._scan_repetition(doc, rule))
            else:
                for sentence in doc.sentences:
                    spans.extend(self._scan_sentence(doc, sentence, rule))

        # canonical order, so two runs over the same document produce identical output
        spans.sort(key=lambda s: (s.start_char, s.end_char, s.rule_id))
        return RuleClassificationResult(document_id=doc.document_id, spans=spans)
