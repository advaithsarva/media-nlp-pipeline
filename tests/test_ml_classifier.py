"""MLClassifier: must be a true no-op with no model file (README.md: models/ is
gitignored and ships nothing), and must never attach a text span or offset to a
prediction -- only rules_engine's exact regex/lexicon matches may do that."""

import numpy as np
import pytest

from nlp_pipeline.ml_classifier import MLClassifier, MLPrediction


def test_unavailable_without_a_model_path():
    clf = MLClassifier(model_path=None, label_map=["a", "b"])
    assert clf.available is False
    assert clf.predict({"x.a": 1.0}) == []


def test_unavailable_when_model_file_is_missing():
    clf = MLClassifier(model_path="models/does_not_exist.onnx", label_map=["a", "b"])
    assert clf.available is False
    assert clf.predict({"x.a": 1.0}) == []


def test_unrecognised_extension_raises():
    with pytest.raises(ValueError):
        MLClassifier(model_path=__file__, label_map=["a"])   # this .py file is not a model


def test_predict_with_no_label_map_returns_empty(tmp_path):
    import joblib
    from sklearn.linear_model import LogisticRegression

    X = np.array([[0.0], [1.0], [0.0], [1.0]])
    y = np.array([0, 1, 0, 1])
    model = LogisticRegression().fit(X, y)
    model_path = tmp_path / "model.joblib"
    joblib.dump(model, model_path)

    clf = MLClassifier(model_path=str(model_path), label_map=[])
    assert clf.predict({"x.a": 1.0}) == []


@pytest.fixture
def trained_sklearn_model(tmp_path):
    import joblib
    from sklearn.linear_model import LogisticRegression

    rng = np.random.RandomState(0)
    X = rng.rand(40, 4)
    y = (X[:, 0] > 0.5).astype(int)
    model = LogisticRegression().fit(X, y)

    path = tmp_path / "model.joblib"
    joblib.dump(model, path)
    return str(path)


def test_sklearn_backend_predicts_a_confidence_per_label(trained_sklearn_model):
    clf = MLClassifier(model_path=trained_sklearn_model, label_map=["negative", "positive"])
    assert clf.available is True
    assert clf.backend == "sklearn"

    bundle = {"a.x1": 0.9, "a.x2": 0.1, "a.x3": 0.5, "a.x4": 0.2}
    predictions = clf.predict(bundle, sentences=[])

    assert len(predictions) == 2
    categories = {p.category for p in predictions}
    assert categories == {"negative", "positive"}
    for p in predictions:
        assert 0.0 <= p.confidence <= 1.0
        assert not hasattr(p, "text")     # never fabricates evidence -- see module docstring
    assert abs(sum(p.confidence for p in predictions) - 1.0) < 1e-6


def test_prediction_is_deterministic(trained_sklearn_model):
    clf = MLClassifier(model_path=trained_sklearn_model, label_map=["negative", "positive"])
    bundle = {"a.x1": 0.9, "a.x2": 0.1, "a.x3": 0.5, "a.x4": 0.2}

    first = clf.predict(bundle, sentences=[])
    second = clf.predict(bundle, sentences=[])
    assert first == second


def test_feature_vector_ignores_non_numeric_and_bool_fields(trained_sklearn_model):
    clf = MLClassifier(model_path=trained_sklearn_model, label_map=["negative", "positive"])
    vector = clf._features_to_vector({
        "a.number": 1.0, "a.text": "ignored", "a.flag": True, "a.none": None, "z.number": 2.0,
    })
    assert list(vector) == [1.0, 2.0]   # sorted by key: 'a.number' < 'z.number'; bool/str/None dropped


def test_sentence_id_attached_when_sentences_given(trained_sklearn_model):
    from nlp_pipeline.shared_types import Sentence

    clf = MLClassifier(model_path=trained_sklearn_model, label_map=["negative", "positive"])
    bundle = {"a.x1": 0.9, "a.x2": 0.1, "a.x3": 0.5, "a.x4": 0.2}

    sentence = Sentence(sentence_id=3, text="x", start_char=0, end_char=1)
    predictions = clf.predict(bundle, sentences=[sentence])
    assert all(p.sentence_id == 3 for p in predictions)

    predictions_no_sentences = clf.predict(bundle, sentences=[])
    assert all(p.sentence_id == -1 for p in predictions_no_sentences)


def test_mlprediction_equality():
    a = MLPrediction(0, "loaded_language", 0.5)
    b = MLPrediction(0, "loaded_language", 0.5)
    c = MLPrediction(0, "loaded_language", 0.6)
    assert a == b
    assert a != c
