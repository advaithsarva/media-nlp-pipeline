"""Detector tests.

The false-positive test is the important one. A detector that fires on a dry factual
paragraph is worse than no detector at all, because it teaches the reader to ignore the
output. Every category gets checked against neutral text here, and any new category must
be added to the same check before it ships.
"""

import pytest

from conftest import NEUTRAL_TEXT, LOADED_TEXT


def test_nothing_fires_on_neutral_text(engine, build_doc):
    doc = build_doc(NEUTRAL_TEXT)
    result = engine.classify(doc)

    assert result.spans == [], (
        "detectors fired on a factual paragraph: "
        + ", ".join(s.category + "=" + repr(s.text) for s in result.spans)
    )


@pytest.mark.parametrize("category", [
    "loaded_language",
    "name_calling",
    "bandwagon",
    "unsupported_quantifier",
    "source_opaqueness",
])
def test_each_category_can_fire(engine, build_doc, category):
    result = engine.classify(build_doc(LOADED_TEXT))

    assert result.spans_for(category), category + " found nothing in the loaded example"


def test_every_span_is_a_verbatim_substring(engine, build_doc):
    doc = build_doc(LOADED_TEXT)
    result = engine.classify(doc)

    for span in result.spans:
        assert doc.text[span.start_char:span.end_char] == span.text


def test_spans_come_back_in_document_order(engine, build_doc):
    result = engine.classify(build_doc(LOADED_TEXT))
    starts = [s.start_char for s in result.spans]

    assert starts == sorted(starts)


def test_same_input_gives_the_same_spans(engine, build_doc):
    first = engine.classify(build_doc(LOADED_TEXT))
    second = engine.classify(build_doc(LOADED_TEXT))

    assert first.spans == second.spans


def test_word_boundaries_are_respected(engine, build_doc):
    # "familiar" contains "liar"; "assassin" contains "ass". Neither may match.
    result = engine.classify(build_doc("The familiar route was assessed by the assembly."))

    assert result.spans == []


def test_every_span_carries_a_rule_id(engine, build_doc):
    result = engine.classify(build_doc(LOADED_TEXT))

    for span in result.spans:
        assert span.rule_id.startswith(span.category + ":")
