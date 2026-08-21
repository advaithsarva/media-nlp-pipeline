"""Preprocessing must annotate the text without ever changing it."""

import unicodedata

from nlp_pipeline.preprocessing import TextProcessor


def test_text_is_not_rewritten():
    processor = TextProcessor()
    text = "  The  MAYOR  said:   'It's fine.'  "

    doc = _fake_document(text)
    result = processor.normalize(doc)

    # no lowercasing, no whitespace collapsing, no trimming
    assert result.text == text


def test_token_offsets_point_at_the_real_word():
    processor = TextProcessor()
    text = "The mayor didn't resign, and the council agreed."

    for token in processor._tokenize(text):
        assert text[token.idx:token.idx + len(token.text)] == token.text


def test_lowercase_and_stopword_are_labels_not_edits():
    processor = TextProcessor()
    tokens = processor._tokenize("The Mayor resigned.")
    by_text = {t.text: t for t in tokens}

    assert by_text["The"].text == "The"        # original spelling kept
    assert by_text["The"].lower == "the"       # lowercase available as a label
    assert by_text["The"].is_stop is True
    assert by_text["Mayor"].is_stop is False
    assert by_text["."].is_punct is True


def test_normalisation_is_idempotent():
    processor = TextProcessor()
    # 'e' followed by a combining acute accent -- NFC turns this into one character
    text = "café opened"

    once = processor._normalize_unicode(text)
    twice = processor._normalize_unicode(once)

    assert once == twice
    assert once == unicodedata.normalize("NFC", text)


def test_word_count_ignores_punctuation():
    processor = TextProcessor()
    doc = _fake_document("Two words, plus punctuation.")
    result = processor.normalize(doc)

    assert result.word_count == 4       # Two, words, plus, punctuation


def _fake_document(text):
    """A minimal stand-in for an InternalDocument, so this test needs no ingestion."""
    from core.internal_document import InternalDocument, SourceType

    return InternalDocument(
        document_id="test",
        text=text,
        source_type=SourceType.FILE_TXT,
        ingestion_timestamp="2026-01-01T00:00:00+00:00",
    )
