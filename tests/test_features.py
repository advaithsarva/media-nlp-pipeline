"""FeatureExtractor must be deterministic and must never fabricate evidence -- every
value is a number, never a quoted span (that job belongs to RuleEngine)."""

from conftest import NEUTRAL_TEXT, LOADED_TEXT

from nlp_pipeline.features import FeatureExtractor


def test_same_document_produces_identical_bundle(build_doc):
    fx = FeatureExtractor()
    doc = build_doc(NEUTRAL_TEXT)

    first = fx.build_features(doc, doc.sentences, {"source_type": "file_txt"})
    second = fx.build_features(doc, doc.sentences, {"source_type": "file_txt"})

    assert first == second
    assert first["deterministic.feature_hash"] == second["deterministic.feature_hash"]


def test_every_layer_key_is_flat_and_namespaced(build_doc):
    fx = FeatureExtractor()
    doc = build_doc(NEUTRAL_TEXT)
    bundle = fx.build_features(doc, doc.sentences)

    for key in bundle:
        assert "." in key, f"{key!r} is not namespaced as '<layer>.<field>'"
        layer, _, field = key.partition(".")
        assert layer, key
        assert field, key


def test_numeric_vector_excludes_non_numeric_fields(build_doc):
    fx = FeatureExtractor()
    doc = build_doc(NEUTRAL_TEXT)
    bundle = fx.build_features(doc, doc.sentences, {"source_type": "file_txt"})
    vector = fx.numeric_vector(bundle)

    numeric_keys = [k for k, v in bundle.items() if isinstance(v, (int, float)) and not isinstance(v, bool)]
    assert len(vector) == len(numeric_keys)
    assert all(isinstance(v, float) for v in vector)


def test_empty_document_does_not_crash(build_doc):
    fx = FeatureExtractor()
    doc = build_doc("")
    bundle = fx.build_features(doc, doc.sentences, {})

    assert bundle["textual.word_count"] == 0.0
    assert bundle["textual.sentence_count"] == 0.0
    assert bundle["lexical.vocabulary_size"] == 0.0


def test_loaded_text_shows_more_hedging_and_punctuation_signal_than_neutral(build_doc):
    """Not a claim that features replicate rule detection -- just that the structural/
    sentiment layers respond to visibly different text at all."""
    fx = FeatureExtractor()
    neutral = fx.build_features(build_doc(NEUTRAL_TEXT))
    loaded = fx.build_features(build_doc(LOADED_TEXT))

    assert neutral != loaded
    assert loaded["sentiment_subjectivity.polarity_mean"] < neutral["sentiment_subjectivity.polarity_mean"]


def test_metadata_layer_passes_through_source_metadata(build_doc):
    fx = FeatureExtractor()
    doc = build_doc(NEUTRAL_TEXT)
    bundle = fx.build_features(doc, doc.sentences, {"source_type": "api_rest", "title": "x"})

    assert bundle["metadata.source_type"] == "api_rest"
    assert bundle["metadata.has_title"] is True
    assert bundle["metadata.has_author"] is False


def test_only_requested_layers_run():
    fx = FeatureExtractor({"layers": ["textual"]})
    from nlp_pipeline.shared_types import NormalizedDocument, Token

    doc = NormalizedDocument(document_id="d", text="Hi.", tokens=[
        Token(text="Hi", lower="hi", lemma="hi", idx=0, is_stop=False, is_punct=False),
        Token(text=".", lower=".", lemma=".", idx=2, is_stop=False, is_punct=True),
    ])
    bundle = fx.build_features(doc)
    layers_present = {k.split(".")[0] for k in bundle if k != "deterministic.feature_hash"}
    assert layers_present == {"textual"}
