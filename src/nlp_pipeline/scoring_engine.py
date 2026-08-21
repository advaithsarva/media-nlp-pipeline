"""Turns evidence spans into one number per category.

The rule that shapes this module: a score is only allowed to depend on evidence that was
actually quoted. Nothing here looks at the text again, only at the spans the rule engine
produced -- which means anyone holding the output can recompute every number in it by
hand and get the same answer.

There is deliberately no overall "bias score". See conf/scoring_v1.yaml for why.
"""

import math

from nlp_pipeline.shared_types import CategoryScore, ScoredDocument


class ScoringEngine:
    def __init__(self, scoring_conf, taxonomy):
        conf = scoring_conf.get("scoring", {})
        self.lam = float(conf.get("lambda", 4.0))
        self.beta = float(conf.get("beta", 0.5))
        self.round_places = int(conf.get("round_places", 6))
        self.expose_composite = bool(conf.get("expose_composite", False))
        self.weights = scoring_conf.get("category_weights", {}) or {}
        self.taxonomy = taxonomy

    def _score_one(self, raw: float, word_count: int) -> float:
        if raw <= 0:
            return 0.0
        # max(...,1) guards against a divide-by-zero on an empty document
        density = raw / (max(word_count, 1) ** self.beta)
        return 1.0 - math.exp(-self.lam * density)

    def score(self, result, doc) -> ScoredDocument:
        word_count = doc.word_count
        scores = {}

        # every category in the taxonomy gets an entry, including the ones that found
        # nothing -- a stable output shape is easier to validate and to diff
        for cat in self.taxonomy.categories:
            spans = result.spans_for(cat.id)
            weight = float(self.weights.get(cat.id, 1.0))
            raw = sum(s.confidence for s in spans) * weight
            scores[cat.id] = CategoryScore(
                category=cat.id,
                count=len(spans),
                raw=round(raw, self.round_places),
                score=round(self._score_one(raw, word_count), self.round_places),
                calibrated=False,
            )

        return ScoredDocument(
            document_id=result.document_id,
            spans=result.spans,
            category_scores=scores,
            composite=None if not self.expose_composite else self._composite(scores),
        )

    def _composite(self, scores):
        # Only reachable if someone flips expose_composite on. Plain mean, not the
        # noisy-OR from the original design: that assumes the categories are independent,
        # and they co-occur heavily, so it saturates towards 1 on ordinary emotive writing.
        values = [c.score for c in scores.values()]
        return round(sum(values) / len(values), self.round_places) if values else 0.0
