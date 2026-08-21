"""Runs the taxonomy's lexicons and regexes over the text and returns evidence spans.

Two properties matter more than coverage here:

1. Every hit carries the exact substring plus its start and end position in the original
   document, so a reader can check the claim against the article. Nothing is paraphrased.
2. The same document always produces the same spans in the same order. Categories,
   sentences and patterns are all walked in a fixed order, and the result is sorted
   before it is returned.
"""

import re

from nlp_pipeline.shared_types import EvidenceSpan, RuleClassificationResult, NormalizedDocument


class RuleEngine:
    def __init__(self, taxonomy, threshold=None):
        self.taxonomy = taxonomy
        self.threshold = taxonomy.default_threshold if threshold is None else threshold
        self.rules = self._compile_rules()

    def _compile_rules(self):
        """One compiled regex per rule, paired with the id that will be stamped on its hits."""
        compiled = []
        for cat in self.taxonomy.categories:
            if cat.detector == "lexicon":
                # \b is a word boundary: it stops "liar" matching inside "familiar".
                pattern = r"\b(?:" + "|".join(re.escape(t) for t in cat.terms) + r")\b"
                compiled.append((cat, f"{cat.id}:lexicon", re.compile(pattern, re.IGNORECASE)))
            else:
                for i, pattern in enumerate(cat.patterns):
                    compiled.append((cat, f"{cat.id}:regex:{i}", re.compile(pattern, re.IGNORECASE)))
        return compiled

    def classify(self, doc: NormalizedDocument) -> RuleClassificationResult:
        spans = []
        for sentence in doc.sentences:
            for cat, rule_id, pattern in self.rules:
                if cat.base_confidence < self.threshold:
                    continue
                for match in pattern.finditer(sentence.text):
                    # match positions are relative to the sentence; add the sentence's
                    # own start to get a position in the whole document
                    start = sentence.start_char + match.start()
                    end = sentence.start_char + match.end()
                    spans.append(EvidenceSpan(
                        text=doc.text[start:end],
                        start_char=start,
                        end_char=end,
                        rule_id=rule_id,
                        category=cat.id,
                        confidence=cat.base_confidence,
                        sentence_id=sentence.sentence_id,
                    ))

        # sorted so two runs over the same document produce byte-identical output
        spans.sort(key=lambda s: (s.start_char, s.end_char, s.rule_id))
        return RuleClassificationResult(document_id=doc.document_id, spans=spans)
