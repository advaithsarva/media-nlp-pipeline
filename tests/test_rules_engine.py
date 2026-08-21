"""Detector tests.

The false-positive tests are the important ones. A detector that fires on a dry factual
paragraph is worse than no detector at all, because it teaches the reader to ignore the
output. Every category is checked against neutral text here, and every new category is
checked automatically -- the parametrised tests read the taxonomy rather than a hard-coded
list, so adding a category without an example or without passing the neutral check fails
the suite.
"""

import pytest

from conftest import NEUTRAL_TEXT, LOADED_TEXT, CATEGORY_EXAMPLES


def _all_category_ids(taxonomy):
    return taxonomy.ids()


def test_nothing_fires_on_neutral_text(engine, build_doc):
    doc = build_doc(NEUTRAL_TEXT)
    result = engine.classify(doc)

    assert result.spans == [], (
        "detectors fired on a factual paragraph: "
        + ", ".join(s.category + "=" + repr(s.text) for s in result.spans)
    )


def test_properly_sourced_writing_does_not_fire(engine, build_doc):
    """The regex_unless detectors exist for exactly this text. None may match it."""
    text = (
        "Support rose by 12% compared with 2019. Many respondents (37%) agreed with the "
        "proposal. Professor Lin of Leeds University said the sample was representative. "
        "According to a 2021 study published in Nature, research shows the effect is small."
    )
    result = engine.classify(build_doc(text))

    assert result.spans == [], ", ".join(
        s.category + "=" + repr(s.text) for s in result.spans)


def test_every_category_has_an_example(taxonomy):
    """A category with no example is a category nobody has proved works."""
    missing = [c for c in taxonomy.ids() if c not in CATEGORY_EXAMPLES]

    assert missing == [], "add an example to conftest.CATEGORY_EXAMPLES for: " + str(missing)


@pytest.mark.parametrize("category", sorted(CATEGORY_EXAMPLES))
def test_each_category_fires_on_its_example(engine, build_doc, category):
    result = engine.classify(build_doc(CATEGORY_EXAMPLES[category]))

    assert result.spans_for(category), (
        category + " found nothing in: " + repr(CATEGORY_EXAMPLES[category]))


@pytest.mark.parametrize("category", sorted(CATEGORY_EXAMPLES))
def test_each_example_is_quoted_verbatim(engine, build_doc, category):
    text = CATEGORY_EXAMPLES[category]
    doc = build_doc(text)

    for span in engine.classify(doc).spans:
        assert text[span.start_char:span.end_char] == span.text


def test_supported_quantifier_is_left_alone(engine, build_doc):
    """The whole point of regex_unless: the same phrase, with and without its evidence."""
    unsupported = engine.classify(build_doc("Many people are worried about the change."))
    supported = engine.classify(build_doc("Many people (61% of 2,400 surveyed) were worried."))

    assert unsupported.spans_for("unsupported_quantifier")
    assert supported.spans_for("unsupported_quantifier") == []


def test_named_authority_is_left_alone(engine, build_doc):
    vague = engine.classify(build_doc("Experts say the bridge is safe."))
    named = engine.classify(build_doc("Experts say the bridge is safe, according to a 2019 review."))

    assert vague.spans_for("appeal_to_authority")
    assert named.spans_for("appeal_to_authority") == []


def test_a_single_virtue_word_is_not_a_slogan(engine, build_doc):
    """Glittering generalities needs two virtue words in a short sentence, not one."""
    explained = engine.classify(build_doc(
        "We need economic justice because current disparities have widened since 2008."))
    slogan = engine.classify(build_doc("Freedom and justice for all!"))

    assert explained.spans_for("glittering_generalities") == []
    assert slogan.spans_for("glittering_generalities")


def test_repetition_reports_one_span_per_occurrence(engine, build_doc):
    """The n-gram window slides, so overlapping matches must be collapsed."""
    result = engine.classify(build_doc(CATEGORY_EXAMPLES["repetition"]))
    spans = result.spans_for("repetition")

    assert len(spans) == 3          # the slogan appears three times, not once per n-gram
    for a, b in zip(spans, spans[1:]):
        assert a.end_char <= b.start_char


def test_stopword_only_phrases_do_not_count_as_repetition(engine, build_doc):
    text = ("The report of the year is here. A copy of the year was sent. "
            "One more of the year arrived. Nothing of the year remains.")
    result = engine.classify(build_doc(text))

    assert result.spans_for("repetition") == []


def test_every_span_is_a_verbatim_substring(engine, build_doc):
    doc = build_doc(LOADED_TEXT)

    for span in engine.classify(doc).spans:
        assert doc.text[span.start_char:span.end_char] == span.text


def test_spans_come_back_in_document_order(engine, build_doc):
    starts = [s.start_char for s in engine.classify(build_doc(LOADED_TEXT)).spans]

    assert starts == sorted(starts)


def test_same_input_gives_the_same_spans(engine, build_doc):
    first = engine.classify(build_doc(LOADED_TEXT))
    second = engine.classify(build_doc(LOADED_TEXT))

    assert first.spans == second.spans


def test_word_boundaries_are_respected(engine, build_doc):
    # "familiar" contains "liar"; "assembly" contains "ass". Neither may match.
    result = engine.classify(build_doc("The familiar route was assessed by the assembly."))

    assert result.spans == []


def test_every_span_carries_a_rule_id(engine, build_doc):
    for span in engine.classify(build_doc(LOADED_TEXT)).spans:
        assert span.rule_id.startswith(span.category + ":")


def test_a_detector_below_threshold_never_emits(taxonomy, build_doc):
    """The R2 gate. Raise the bar above every category and nothing may come out."""
    from nlp_pipeline.rules_engine import RuleEngine

    strict = RuleEngine(taxonomy, threshold=0.99)

    assert strict.classify(build_doc(LOADED_TEXT)).spans == []
