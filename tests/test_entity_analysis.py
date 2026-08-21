"""The spaCy entity stage and the two detectors that depend on it.

Determinism matters more here than anywhere else in the pipeline, because this is the only
stage backed by a statistical model. spaCy inference has no dropout and no sampling, so it
is reproducible -- but that is a claim worth testing rather than asserting.
"""

import pytest

from conftest import NEUTRAL_TEXT

spacy = pytest.importorskip("spacy")
pytest.importorskip("vaderSentiment")

from nlp_pipeline.entity_analysis import EntityAnalyzer      # noqa: E402


SCAPEGOAT_TEXT = (
    "Migrants are blamed for the housing shortage. The council met on Tuesday. "
    "Migrants are also responsible for rising crime, the leader said. "
    "Migrants caused the strain on hospitals too."
)

CARD_STACKING_TEXT = (
    "Fairhaven Trust delivered an outstanding, wonderful result and its staff were "
    "praised as excellent. Fairhaven Trust was celebrated again for its brilliant work. "
    "Northgate Group produced a terrible failure and its staff were condemned. "
    "Northgate Group was criticised again for its awful record."
)


# ---- the stage itself ----

def test_entity_offsets_slice_back_to_the_entity(build_doc):
    doc = build_doc(CARD_STACKING_TEXT)

    assert doc.entities, "spaCy found no entities"
    for entity in doc.entities:
        assert doc.text[entity.start_char:entity.end_char] == entity.text


def test_every_entity_lands_in_a_sentence(build_doc):
    doc = build_doc(CARD_STACKING_TEXT)

    for entity in doc.entities:
        assert entity.sentence_id >= 0
        sentence = doc.sentences[entity.sentence_id]
        assert sentence.start_char <= entity.start_char < sentence.end_char


def test_entities_come_back_in_document_order(build_doc):
    doc = build_doc(CARD_STACKING_TEXT)
    starts = [e.start_char for e in doc.entities]

    assert starts == sorted(starts)


def test_the_same_text_gives_the_same_entities(build_doc):
    """spaCy is a statistical model; inference must still be reproducible."""
    first = build_doc(CARD_STACKING_TEXT)
    second = build_doc(CARD_STACKING_TEXT)

    assert first.entities == second.entities
    assert first.entity_sentiment == second.entity_sentiment


def test_sentiment_separates_the_two_sides(build_doc):
    doc = build_doc(CARD_STACKING_TEXT)

    warm = doc.entity_sentiment["fairhaven trust"]["average_sentiment"]
    cold = doc.entity_sentiment["northgate group"]["average_sentiment"]

    assert warm > 0.5
    assert cold < -0.5


def test_the_model_version_is_recorded(build_doc):
    """A different spaCy model finds different entities, so the output must say which ran."""
    doc = build_doc(CARD_STACKING_TEXT)

    assert doc.metadata["entity_model"].startswith("en_core_web_sm:")


def test_entity_keys_ignore_a_leading_article():
    analyzer = EntityAnalyzer()

    assert analyzer._entity_key("The Northgate Group") == "northgate group"
    assert analyzer._entity_key("  northgate   group ") == "northgate group"


# ---- scapegoating ----

def test_scapegoating_fires_on_a_repeatedly_blamed_group(engine, build_doc):
    result = engine.classify(build_doc(SCAPEGOAT_TEXT))
    spans = result.spans_for("scapegoating")

    # Two, not three. The text blames migrants in three sentences, but "Migrants caused
    # the strain" uses a causal verb, and "caused" was removed from the blame lexicon
    # after it produced "caused by the bacterium Yersinia pestis" on real text.
    assert len(spans) == 2
    assert all(s.text == "Migrants" for s in spans)


def test_scapegoating_needs_more_than_one_sentence(engine, build_doc):
    """One accusation is reporting. A pattern of them is scapegoating."""
    once = ("Migrants are blamed by some for the housing shortage. "
            "The council met on Tuesday and approved 400 new homes.")
    result = engine.classify(build_doc(once))

    assert result.spans_for("scapegoating") == []


def test_repeated_mentions_in_one_sentence_are_one_accusation(engine, build_doc):
    text = "Migrants, migrants and migrants again are blamed for the shortage."
    result = engine.classify(build_doc(text))

    assert result.spans_for("scapegoating") == []


def test_scapegoating_needs_a_blame_phrase(engine, build_doc):
    """Mentioning a group repeatedly is not blaming it."""
    neutral = ("Migrants arrived in the county in March. Migrants were housed in three "
               "centres. Migrants received language classes from the council.")
    result = engine.classify(build_doc(neutral))

    assert result.spans_for("scapegoating") == []


def test_scapegoating_catches_named_groups_too(engine, build_doc):
    """group_terms covers unnamed groups; spaCy NER covers the named ones."""
    text = ("Muslims are blamed for the unrest by the newspaper. "
            "The weather stayed dry. "
            "Muslims are responsible for the tension, the column argued.")
    result = engine.classify(build_doc(text))

    assert result.spans_for("scapegoating")


# ---- card stacking ----

def test_card_stacking_fires_on_an_asymmetric_pair(engine, build_doc):
    result = engine.classify(build_doc(CARD_STACKING_TEXT))
    spans = result.spans_for("card_stacking")

    quoted = {s.text for s in spans}
    assert "Fairhaven Trust" in quoted      # the warm end
    assert "Northgate Group" in quoted      # and the cold end, both quoted


def test_warmth_towards_everyone_is_not_card_stacking(engine, build_doc):
    both_warm = ("Fairhaven Trust delivered an outstanding result and staff were praised. "
                 "Northgate Group also produced an excellent, wonderful outcome. "
                 "Fairhaven Trust was celebrated again. Northgate Group was praised again.")
    result = engine.classify(build_doc(both_warm))

    assert result.spans_for("card_stacking") == []


def test_balanced_reporting_is_not_card_stacking(engine, build_doc):
    balanced = ("Fairhaven Trust reported a 4% rise in admissions. "
                "Northgate Group reported a 2% fall. "
                "Fairhaven Trust said the figures matched forecasts. "
                "Northgate Group declined to comment on the quarter.")
    result = engine.classify(build_doc(balanced))

    assert result.spans_for("card_stacking") == []


def test_a_single_mention_is_not_enough(engine, build_doc):
    """min_mentions: one passing mention in one emotive sentence is not a stance."""
    text = ("Fairhaven Trust delivered an outstanding, wonderful result. "
            "Northgate Group produced a terrible, disgraceful failure.")
    result = engine.classify(build_doc(text))

    assert result.spans_for("card_stacking") == []


# ---- neither may fire on neutral text ----

def test_neither_entity_detector_fires_on_neutral_text(engine, build_doc):
    result = engine.classify(build_doc(NEUTRAL_TEXT))

    assert result.spans_for("scapegoating") == []
    assert result.spans_for("card_stacking") == []


def test_entity_detectors_stay_quiet_without_the_entity_stage(taxonomy):
    """A document that never went through the entity stage must produce no guesses."""
    from nlp_pipeline.preprocessing import TextProcessor
    from nlp_pipeline.segmentation import SentenceSegmenter
    from nlp_pipeline.rules_engine import RuleEngine
    from nlp_pipeline.shared_types import NormalizedDocument

    doc = NormalizedDocument("x", CARD_STACKING_TEXT,
                             TextProcessor()._tokenize(CARD_STACKING_TEXT))
    SentenceSegmenter().segment(doc)     # no EntityAnalyzer

    result = RuleEngine(taxonomy).classify(doc)

    assert result.spans_for("card_stacking") == []
    assert result.spans_for("scapegoating") == []
