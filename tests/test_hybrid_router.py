"""HybridRouter: rules must always win when they fire, ML confidence may only adjust an
already-quoted finding's confidence (never its text/offsets), and an ML-only category
must never be reported as if it were quoted evidence."""

import pytest

from nlp_pipeline.hybrid_router import HybridRouter
from nlp_pipeline.ml_classifier import MLPrediction
from nlp_pipeline.ontology_graph import OntologyGraph
from nlp_pipeline.shared_types import EvidenceSpan, RuleClassificationResult


def _span(category, confidence, sentence_id=0):
    return EvidenceSpan(
        text="disastrous", start_char=0, end_char=10, rule_id=category + ":lexicon",
        category=category, confidence=confidence, sentence_id=sentence_id,
    )


@pytest.fixture
def ontology(taxonomy):
    return OntologyGraph(taxonomy)


def test_pass_through_with_no_ml_result(ontology):
    router = HybridRouter({}, ontology)
    rule_result = RuleClassificationResult(document_id="d", spans=[_span("loaded_language", 0.85)])

    merged = router.merge(rule_result, None, ontology)

    assert len(merged.spans) == 1
    assert merged.spans[0].confidence == 0.85
    assert merged.spans[0].text == "disastrous"      # untouched
    assert merged.unconfirmed_categories == {}


def test_rule_span_above_threshold_is_never_blended(ontology):
    router = HybridRouter({"alpha": 0.5, "confidence_threshold": 0.5}, ontology)
    rule_result = RuleClassificationResult(document_id="d", spans=[_span("loaded_language", 0.9)])
    ml_result = [MLPrediction(0, "loaded_language", 0.1)]

    merged = router.merge(rule_result, ml_result, ontology)

    assert merged.spans[0].confidence == 0.9


def test_rule_span_below_threshold_blends_with_alpha(ontology):
    router = HybridRouter({"alpha": 0.5, "confidence_threshold": 0.95}, ontology)
    rule_result = RuleClassificationResult(document_id="d", spans=[_span("loaded_language", 0.85)])
    ml_result = [MLPrediction(0, "loaded_language", 0.4)]

    merged = router.merge(rule_result, ml_result, ontology)

    assert merged.spans[0].confidence == pytest.approx(0.5 * 0.85 + 0.5 * 0.4)
    assert merged.spans[0].text == "disastrous"      # blending changes confidence only


def test_alpha_one_ignores_ml_entirely(ontology):
    router = HybridRouter({"alpha": 1.0, "confidence_threshold": 0.95}, ontology)
    rule_result = RuleClassificationResult(document_id="d", spans=[_span("loaded_language", 0.85)])
    ml_result = [MLPrediction(0, "loaded_language", 0.0)]

    merged = router.merge(rule_result, ml_result, ontology)
    assert merged.spans[0].confidence == 0.85


def test_ml_only_category_is_unconfirmed_not_a_span(ontology):
    router = HybridRouter({"min_unconfirmed_confidence": 0.5}, ontology)
    rule_result = RuleClassificationResult(document_id="d", spans=[])
    ml_result = [MLPrediction(0, "whataboutism", 0.8), MLPrediction(0, "bandwagon", 0.3)]

    merged = router.merge(rule_result, ml_result, ontology)

    assert merged.spans == []
    assert merged.unconfirmed_categories == {"whataboutism": 0.8}   # bandwagon below 0.5, dropped


def test_never_fabricates_a_span_for_an_unconfirmed_category(ontology):
    router = HybridRouter({}, ontology)
    rule_result = RuleClassificationResult(document_id="d", spans=[])
    ml_result = [MLPrediction(0, "whataboutism", 0.99)]

    merged = router.merge(rule_result, ml_result, ontology)

    assert merged.spans_for("whataboutism") == []
    assert "whataboutism" in merged.unconfirmed_categories


def test_unknown_category_from_ml_raises(ontology):
    router = HybridRouter({}, ontology)
    rule_result = RuleClassificationResult(document_id="d", spans=[])
    with pytest.raises(KeyError):
        router.merge(rule_result, [MLPrediction(0, "not_a_real_category", 0.9)], ontology)


def test_unknown_category_from_rules_raises(ontology):
    router = HybridRouter({}, ontology)
    rule_result = RuleClassificationResult(document_id="d", spans=[_span("not_a_real_category", 0.9)])
    with pytest.raises(KeyError):
        router.merge(rule_result, None, ontology)


def test_merged_spans_stay_in_canonical_order(ontology):
    router = HybridRouter({}, ontology)
    late = EvidenceSpan(text="b", start_char=10, end_char=11, rule_id="bandwagon:regex:0",
                        category="bandwagon", confidence=0.9, sentence_id=0)
    early = EvidenceSpan(text="a", start_char=0, end_char=1, rule_id="loaded_language:lexicon",
                         category="loaded_language", confidence=0.9, sentence_id=0)
    rule_result = RuleClassificationResult(document_id="d", spans=[late, early])

    merged = router.merge(rule_result, None, ontology)
    assert [s.start_char for s in merged.spans] == [0, 10]


def test_works_without_an_ontology():
    router = HybridRouter({"alpha": 0.5, "confidence_threshold": 0.95})
    rule_result = RuleClassificationResult(document_id="d", spans=[_span("loaded_language", 0.85)])
    ml_result = [MLPrediction(0, "loaded_language", 0.4)]

    merged = router.merge(rule_result, ml_result)
    assert merged.spans[0].confidence == pytest.approx(0.5 * 0.85 + 0.5 * 0.4)
