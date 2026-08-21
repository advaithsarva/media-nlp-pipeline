"""Scoring must be recomputable by hand from the evidence, and must stay in 0..1."""

import math

from conftest import NEUTRAL_TEXT, LOADED_TEXT


def test_no_evidence_means_zero(engine, scorer, build_doc):
    doc = build_doc(NEUTRAL_TEXT)
    scored = scorer.score(engine.classify(doc), doc)

    for category, score in scored.category_scores.items():
        assert score.count == 0
        assert score.score == 0.0


def test_every_category_appears_even_with_no_hits(engine, scorer, build_doc, taxonomy):
    doc = build_doc(NEUTRAL_TEXT)
    scored = scorer.score(engine.classify(doc), doc)

    assert sorted(scored.category_scores) == sorted(taxonomy.ids())


def test_scores_stay_inside_zero_to_one(engine, scorer, build_doc):
    doc = build_doc(LOADED_TEXT * 20)       # a lot of evidence should saturate, not overflow
    scored = scorer.score(engine.classify(doc), doc)

    for score in scored.category_scores.values():
        assert 0.0 <= score.score <= 1.0


def test_more_evidence_scores_higher(engine, scorer, build_doc):
    small = build_doc("The plan was disastrous.")
    large = build_doc("The plan was disastrous and shameful and ludicrous and appalling.")

    small_score = scorer.score(engine.classify(small), small).category_scores["loaded_language"]
    large_score = scorer.score(engine.classify(large), large).category_scores["loaded_language"]

    assert large_score.score > small_score.score


def test_the_number_can_be_recomputed_from_the_evidence(engine, scorer, build_doc):
    """This is the property the whole design is for: no unexplainable numbers."""
    doc = build_doc(LOADED_TEXT)
    result = engine.classify(doc)
    scored = scorer.score(result, doc)

    for category, score in scored.category_scores.items():
        raw = sum(s.confidence for s in result.spans_for(category))
        density = raw / (max(doc.word_count, 1) ** scorer.beta)
        expected = 0.0 if raw <= 0 else 1.0 - math.exp(-scorer.lam * density)

        assert score.score == round(expected, scorer.round_places)


def test_no_composite_is_exposed(engine, scorer, build_doc):
    doc = build_doc(LOADED_TEXT)
    scored = scorer.score(engine.classify(doc), doc)

    assert scored.composite is None
    assert all(not s.calibrated for s in scored.category_scores.values())


# ---- severity, disruption and the composites ----

def test_severity_uses_the_category_weight(engine, scorer, build_doc, taxonomy):
    """s_i = confidence * severity_weight, per instance."""
    doc = build_doc("The minister is a liar and a charlatan.")
    scored = scorer.score(engine.classify(doc), doc)

    entry = scored.severity["per_category"]["name_calling"]
    weight = taxonomy.by_id("name_calling").severity_weight
    expected = 0.85 * weight        # base_confidence of the name_calling detector

    assert entry["severity_weight"] == weight
    assert abs(entry["max_instance_severity"] - expected) < 1e-6


def test_repeated_instances_accumulate_but_saturate(engine, scorer, build_doc):
    """1 - exp(-n): five ad hominems are worse than one, but not five times worse."""
    once = build_doc("The minister is a liar.")
    many = build_doc("A liar, a crook, a charlatan, a coward and a hypocrite.")

    one = scorer.score(engine.classify(once), once).severity["per_category"]["name_calling"]
    five = scorer.score(engine.classify(many), many).severity["per_category"]["name_calling"]

    assert five["accumulated_severity"] > one["accumulated_severity"]
    assert five["accumulated_severity"] < 5 * one["accumulated_severity"]
    assert five["accumulated_severity"] <= 1.0


def test_coherence_is_one_minus_disruption(engine, scorer, build_doc):
    doc = build_doc(LOADED_TEXT)
    severity = scorer.score(engine.classify(doc), doc).severity

    assert abs(severity["coherence"] + severity["logical_flow_disruption"] - 1.0) < 1e-6


def test_clean_text_has_perfect_coherence(engine, scorer, build_doc):
    doc = build_doc(NEUTRAL_TEXT)
    severity = scorer.score(engine.classify(doc), doc).severity

    assert severity["logical_flow_disruption"] == 0.0
    assert severity["coherence"] == 1.0
    assert severity["per_category"] == {}


def test_the_additive_total_is_the_sum_of_its_breakdown(engine, scorer, build_doc):
    """The most checkable composite: the total must literally be the visible list added up."""
    doc = build_doc(LOADED_TEXT)
    additive = scorer.score(engine.classify(doc), doc).composites["additive_manipulation"]

    expected = min(sum(additive["breakdown"].values()), 1.0)

    assert abs(additive["value"] - expected) < 1e-6
    assert additive["band"] in ("low", "moderate", "high")


def test_hedging_never_counts_as_manipulation(engine, scorer, build_doc):
    """Hedging is style, not a fault -- it is in the excluded family."""
    doc = build_doc("The change may possibly reduce costs, which suggests a saving.")
    scored = scorer.score(engine.classify(doc), doc)

    assert scored.category_scores["hedging"].count > 0
    assert "hedging" not in scored.composites["additive_manipulation"]["breakdown"]
    assert scored.composites["additive_manipulation"]["value"] == 0.0


def test_noisy_or_saturates_where_smooth_max_does_not(configs, taxonomy, engine, build_doc):
    """The F1 result, as a test: the original formula compounds correlated evidence.

    Same document, same evidence, two aggregators. noisy_or must come out substantially
    higher -- that gap is the miscalibration the smooth-max replacement exists to fix.
    """
    import copy
    from nlp_pipeline.scoring_engine import ScoringEngine

    doc = build_doc(LOADED_TEXT)
    result = engine.classify(doc)

    scores = {}
    for method in ("smooth_max", "noisy_or"):
        conf = copy.deepcopy(configs[2])
        conf["scoring"]["prop_score_method"] = method
        scored = ScoringEngine(conf, taxonomy).score(result, doc)
        scores[method] = scored.composites["prop_score"]["value"]
        assert scored.composites["prop_score"]["method"] == method

    assert scores["noisy_or"] > scores["smooth_max"]
    assert 0.0 <= scores["smooth_max"] <= 1.0
    assert 0.0 <= scores["noisy_or"] <= 1.0


def test_every_composite_ships_its_working(engine, scorer, build_doc):
    doc = build_doc(LOADED_TEXT)
    composites = scorer.score(engine.classify(doc), doc).composites

    assert composites["calibrated"] is False
    assert "uncalibrated" in composites["warning"].lower()
    for name in ("prop_score", "fallacy_score", "bias_signal", "manipulation_index"):
        assert "inputs" in composites[name]
    assert "breakdown" in composites["additive_manipulation"]


def test_composites_stay_inside_zero_to_one(engine, scorer, build_doc):
    doc = build_doc(LOADED_TEXT * 30)
    composites = scorer.score(engine.classify(doc), doc).composites

    for name in ("prop_score", "fallacy_score", "bias_signal",
                 "additive_manipulation", "manipulation_index", "article_score"):
        assert 0.0 <= composites[name]["value"] <= 1.0


def test_turning_expose_composite_on_publishes_the_number(configs, taxonomy, engine, build_doc):
    import copy
    from nlp_pipeline.scoring_engine import ScoringEngine

    doc = build_doc(LOADED_TEXT)
    result = engine.classify(doc)

    conf = copy.deepcopy(configs[2])
    conf["scoring"]["expose_composite"] = True
    scored = ScoringEngine(conf, taxonomy).score(result, doc)

    assert scored.composite is not None
    assert scored.composite == scored.composites["additive_manipulation"]["value"]
