"""Sentence offsets are load-bearing: every quote the pipeline reports is built from them."""

from conftest import NEUTRAL_TEXT


def test_offsets_slice_back_to_the_sentence(build_doc):
    doc = build_doc(NEUTRAL_TEXT)

    assert doc.sentences, "no sentences were produced"
    for sentence in doc.sentences:
        assert doc.text[sentence.start_char:sentence.end_char] == sentence.text


def test_abbreviations_do_not_split_a_sentence(build_doc):
    doc = build_doc("Dr. Smith met Mr. Jones on Mon. They agreed.")

    assert len(doc.sentences) == 2
    assert doc.sentences[0].text == "Dr. Smith met Mr. Jones on Mon."


def test_hard_wrapped_lines_are_one_sentence(build_doc):
    # a plain-text file wrapped at column 40 -- the line break is not a sentence end
    text = "The council said that every\nsingle objection had been considered."
    doc = build_doc(text)

    assert len(doc.sentences) == 1
    assert doc.sentences[0].text == text


def test_blank_line_still_separates(build_doc):
    doc = build_doc("A headline with no full stop\n\nThe body begins here.")

    assert len(doc.sentences) == 2


def test_sentence_ids_are_sequential(build_doc):
    doc = build_doc(NEUTRAL_TEXT)

    assert [s.sentence_id for s in doc.sentences] == list(range(len(doc.sentences)))


def test_no_leading_or_trailing_whitespace(build_doc):
    doc = build_doc(NEUTRAL_TEXT)

    for sentence in doc.sentences:
        assert sentence.text == sentence.text.strip()
