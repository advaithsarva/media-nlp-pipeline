"""Tier 3 of README.md's Classification Tiers table: merges the rule engine's evidence
spans with the ML classifier's confidence scores.

    if rule_confidence >= threshold:
        return rule_result
    else:
        blended = alpha * conf_rules + (1 - alpha) * conf_ml
        return assign_labels(blended, thresholds)

Rules always win when they fire. A rule hit carries an exact, quotable substring; an ML
prediction is a bare confidence number with no evidence attached (see `ml_classifier.py`).
Overriding a quoted finding with an unquotable one would make the output less trustworthy,
not more -- so `HybridRouter` never removes a rule span, and it never invents one either:
what ML confidence can do is raise the *confidence already attached to a category the
rules already found*, or record a low-confidence, evidence-free signal for a category the
rules missed entirely. That second case is surfaced separately, as
`unconfirmed_categories`, rather than folded into `spans`, so a consumer can never
mistake an ML-only guess for a quoted finding by iterating `spans` alone.

`ontology_graph` is consulted only to check that every category name either side produced
is a real taxonomy category (`validate_label_set`) -- a stale or misspelled label fails
loudly here rather than silently scoring as zero three stages later.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from nlp_pipeline.ontology_graph import OntologyGraph
from nlp_pipeline.shared_types import EvidenceSpan, RuleClassificationResult


@dataclass
class HybridResult:
    document_id: str
    spans: List[EvidenceSpan] = field(default_factory=list)
    # category -> the confidence HybridRouter settled on, after blending where it applied.
    # Includes every category a rule span carries, so this is a superset of
    # {s.category for s in spans}, keyed to the same confidence values a consumer would
    # otherwise have to recompute from spans by hand.
    confidences: Dict[str, float] = field(default_factory=dict)
    # Categories the ML classifier flagged that no rule found any evidence for. Reported
    # separately from `spans` on purpose -- see the module docstring.
    unconfirmed_categories: Dict[str, float] = field(default_factory=dict)

    def spans_for(self, category: str) -> List[EvidenceSpan]:
        return [s for s in self.spans if s.category == category]


class HybridRouter:
    def __init__(self, hybrid_config: Dict[str, Any], ontology_graph: Optional[OntologyGraph] = None):
        config = hybrid_config or {}
        self.alpha = float(config.get("alpha", 1.0))
        # Below this, a rule's own confidence is treated as "not confident enough" and
        # ML gets a say. Independent of the taxonomy-wide `default_threshold` in
        # taxonomy_v1.yaml, which decides whether a rule fires *at all* -- this decides
        # whether a rule that already fired should be blended with ML.
        self.confidence_threshold = float(config.get("confidence_threshold", 0.7))
        # A category ML flags with less than this is noise, not a signal worth surfacing.
        self.min_unconfirmed_confidence = float(config.get("min_unconfirmed_confidence", 0.5))
        self.ontology = ontology_graph

    def _validate(self, categories) -> None:
        if self.ontology is None or not categories:
            return
        if not self.ontology.validate_label_set(categories):
            unknown = set(categories) - set(self.ontology.categories())
            raise KeyError("HybridRouter received unknown categories: " + ", ".join(sorted(unknown)))

    def _blend(self, rule_confidence: float, ml_confidence: float) -> float:
        return self.alpha * rule_confidence + (1.0 - self.alpha) * ml_confidence

    def merge(self, rule_result: RuleClassificationResult, ml_result=None,
              ontology: Optional[OntologyGraph] = None) -> HybridResult:
        """`ml_result` is whatever `MLClassifier.predict` returned -- a list of
        `MLPrediction`, or `None`/`[]` when no model is loaded, in which case this is a
        pass-through: rule spans and their own confidences, unchanged."""
        ontology = ontology or self.ontology
        ml_result = ml_result or []

        # category -> best ML confidence for that category (predictions can repeat a
        # category across sentences; the strongest one is the one worth blending with)
        ml_by_category: Dict[str, float] = {}
        for prediction in ml_result:
            existing = ml_by_category.get(prediction.category, 0.0)
            ml_by_category[prediction.category] = max(existing, prediction.confidence)

        self._validate(list(ml_by_category))
        self._validate([s.category for s in rule_result.spans])

        merged_spans: List[EvidenceSpan] = []
        confidences: Dict[str, float] = {}

        for span in rule_result.spans:
            ml_confidence = ml_by_category.get(span.category)
            if ml_confidence is not None and span.confidence < self.confidence_threshold:
                blended = self._blend(span.confidence, ml_confidence)
                span = EvidenceSpan(
                    text=span.text, start_char=span.start_char, end_char=span.end_char,
                    rule_id=span.rule_id, category=span.category,
                    confidence=round(blended, 6), sentence_id=span.sentence_id,
                    in_quotation=span.in_quotation,
                )
            merged_spans.append(span)
            confidences[span.category] = max(confidences.get(span.category, 0.0), span.confidence)

        rule_categories = {s.category for s in rule_result.spans}
        unconfirmed = {
            category: round(confidence, 6)
            for category, confidence in ml_by_category.items()
            if category not in rule_categories and confidence >= self.min_unconfirmed_confidence
        }

        merged_spans.sort(key=lambda s: (s.start_char, s.end_char, s.rule_id))
        return HybridResult(
            document_id=rule_result.document_id,
            spans=merged_spans,
            confidences=confidences,
            unconfirmed_categories=unconfirmed,
        )
