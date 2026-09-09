"""Optional ML fallback classifier -- Tier 2 in README.md's Classification Tiers table.

Two things keep this consistent with the rest of the project's precision-first design:

1. It never invents evidence. `RuleEngine` can quote an exact substring because a regex
   match *is* the evidence. A model cannot: it has no way to point at "the part of the
   sentence that made it decide this". So `predict` returns confidence scores per
   (sentence, category) -- a signal `HybridRouter` can use to raise or lower how much a
   near-miss rule result should be trusted -- and never a fabricated `EvidenceSpan`.
   `conf/taxonomy_v1.yaml`'s own header makes the same call for regex-only detectors:
   "never anything that paraphrases".

2. It is a fallback, not a requirement. `models/` is gitignored and nothing ships a
   trained model (see README.md's "Not built" table this module used to belong to), so
   `MLClassifier` has to behave correctly with no model file present: `predict` returns
   an empty result rather than raising, and callers can check `.available` to know
   whether there was ever a model to ask. Point `model_path` at a real artifact -- an
   ONNX export or a joblib-pickled scikit-learn estimator -- and the same class uses it.
"""

from pathlib import Path
from typing import Any, Dict, List

import numpy as np


class MLPrediction:
    """One (sentence, category) confidence the model produced. No text, no offsets --
    see the module docstring for why."""

    __slots__ = ("sentence_id", "category", "confidence")

    def __init__(self, sentence_id: int, category: str, confidence: float):
        self.sentence_id = sentence_id
        self.category = category
        self.confidence = confidence

    def __repr__(self):
        return (f"MLPrediction(sentence_id={self.sentence_id}, category={self.category!r}, "
                f"confidence={self.confidence!r})")

    def __eq__(self, other):
        return (isinstance(other, MLPrediction) and self.sentence_id == other.sentence_id
                and self.category == other.category and self.confidence == other.confidence)


class MLClassifier:
    def __init__(self, model_path: str = None, label_map: List[str] = None):
        self.model_path = model_path
        self.label_map = list(label_map) if label_map else []
        self._session = None
        self._sklearn_model = None
        self.backend = self._resolve_backend()

    # ---------- setup ----------

    def _resolve_backend(self) -> str:
        if not self.model_path or not Path(self.model_path).is_file():
            return "unavailable"
        suffix = Path(self.model_path).suffix.lower()
        if suffix == ".onnx":
            return "onnx"
        if suffix in (".joblib", ".pkl", ".pickle"):
            return "sklearn"
        raise ValueError(f"unrecognised model file type: {self.model_path!r}")

    @property
    def available(self) -> bool:
        return self.backend != "unavailable"

    @property
    def session(self):
        if self._session is None:
            import onnxruntime as ort
            self._session = ort.InferenceSession(self.model_path, providers=["CPUExecutionProvider"])
        return self._session

    @property
    def sklearn_model(self):
        if self._sklearn_model is None:
            import joblib
            self._sklearn_model = joblib.load(self.model_path)
        return self._sklearn_model

    # ---------- feature vector ----------

    def _features_to_vector(self, feature_bundle: Dict[str, Any]) -> np.ndarray:
        """Fixed-order numeric vector from a `FeatureExtractor.build_features` bundle.

        Sorted by key rather than a hard-coded schema: the vector layout then follows
        whichever feature layers are actually enabled, and adding or removing a layer in
        `pipeline_v1.yaml`'s `feature_extraction` section does not require touching this
        class. The trade-off -- a model trained against one layer set silently gets a
        differently-shaped vector if the layer set changes -- is the reason model
        artifacts are version-pinned (README.md, Determinism Model): the feature config
        that produced a model's training data has to travel with it.
        """
        items = sorted(
            (k, v) for k, v in feature_bundle.items()
            if isinstance(v, (int, float)) and not isinstance(v, bool)
        )
        return np.array([float(v) for _, v in items], dtype=np.float64)

    # ---------- inference ----------

    def _predict_onnx(self, vector: np.ndarray) -> np.ndarray:
        input_name = self.session.get_inputs()[0].name
        outputs = self.session.run(None, {input_name: vector.reshape(1, -1).astype(np.float32)})
        probabilities = np.asarray(outputs[0]).reshape(-1)
        return probabilities

    def _predict_sklearn(self, vector: np.ndarray) -> np.ndarray:
        model = self.sklearn_model
        if hasattr(model, "predict_proba"):
            return np.asarray(model.predict_proba(vector.reshape(1, -1))).reshape(-1)
        # no predict_proba (e.g. a plain SVM): fall back to a hard 0/1 vector over the
        # predicted class rather than raising, so predict() always returns confidences
        prediction = model.predict(vector.reshape(1, -1))[0]
        labels = list(getattr(model, "classes_", self.label_map))
        return np.array([1.0 if label == prediction else 0.0 for label in labels])

    def predict(self, feature_bundle: Dict[str, Any], sentences=None) -> List[MLPrediction]:
        """One document-level feature bundle in, one confidence per label out.

        `sentences` is accepted for interface parity with the tiered design in
        README.md (`self.ml.predict(features, sentences)`) and with `HybridRouter.merge`,
        which needs a sentence to attach a prediction to; every prediction here is
        attached to sentence 0 (or to -1, document-level, when there are no sentences),
        because this classifier reasons over one document-level feature bundle, not a
        per-sentence one. A sentence-level model would need a per-sentence feature
        bundle, which is a natural extension once `FeatureExtractor` is asked to build
        one span at a time rather than for the whole document.
        """
        if not self.available or not self.label_map:
            return []

        vector = self._features_to_vector(feature_bundle)
        if self.backend == "onnx":
            probabilities = self._predict_onnx(vector)
        else:
            probabilities = self._predict_sklearn(vector)

        sentence_id = sentences[0].sentence_id if sentences else -1
        n = min(len(self.label_map), len(probabilities))
        return [
            MLPrediction(
                sentence_id=sentence_id, category=self.label_map[i],
                confidence=round(float(probabilities[i]), 6),
            )
            for i in range(n)
        ]
