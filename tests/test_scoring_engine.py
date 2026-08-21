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
