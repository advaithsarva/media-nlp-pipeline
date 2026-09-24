"""Sentence embeddings for semantic similarity -- taxonomy suggestions, near-duplicate
detection, cross-document work. Nothing in the scoring path (`scoring_engine.py`) depends
on this: embeddings are read-only semantic memory, consulted, never a source of evidence,
because a vector cannot be quoted the way `EvidenceSpan.text` can.

Two backends, chosen automatically:

  onnx        `emb_cfg["model_path"]` points at a real ONNX sentence encoder (e.g. an
              exported MiniLM). Used when the file is actually there.
  hashing     No model file -- the default, since `models/` is gitignored and nothing
              ships one (see README.md's "Not built" table this module used to be part
              of). A deterministic bag-of-words feature-hashing embedding: every token is
              hashed into one of `embedding_dim` buckets and the buckets are L2-normalised.
              Not a substitute for a trained encoder's semantics, but it is a real,
              reproducible vector with no network call and no model download -- which is
              what keeps the project's "air-gap compatible" claim (README.md, Operational
              Considerations) true by default.

Both backends produce a vector of exactly `embedding_dim` floats, L2-normalised, so
`VectorIndex` can always use inner product as cosine similarity regardless of which
backend produced the vector.
"""

import hashlib
import re
from typing import Any, Dict, List, Union

import numpy as np

TOKEN_PATTERN = re.compile(r"\w+")


def _l2_normalize(vector: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm


class EmbeddingGenerator:
    def __init__(self, emb_cfg: Dict[str, Any] = None):
        self.config = emb_cfg or {}
        self.embedding_dim = int(self.config.get("embedding_dim", 384))
        self.normalize = bool(self.config.get("normalize", True))
        self.model_path = self.config.get("model_path")
        self.max_length = int(self.config.get("max_length", 512))

        self._session = None
        self._tokenizer = None
        self.backend = self._resolve_backend()

    # ---------- backend selection ----------

    def _resolve_backend(self) -> str:
        if not self.model_path:
            return "hashing"
        from pathlib import Path
        if not Path(self.model_path).is_file():
            return "hashing"
        return "onnx"

    @property
    def session(self):
        if self._session is None:
            import onnxruntime as ort
            self._session = ort.InferenceSession(self.model_path, providers=["CPUExecutionProvider"])
        return self._session

    @property
    def tokenizer(self):
        if self._tokenizer is None:
            from transformers import AutoTokenizer
            tokenizer_source = self.config.get("tokenizer_path", self.model_path)
            self._tokenizer = AutoTokenizer.from_pretrained(tokenizer_source)
        return self._tokenizer

    # ---------- hashing fallback ----------

    def _hash_bucket(self, token: str) -> int:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        return int.from_bytes(digest[:4], "big") % self.embedding_dim

    def _hash_sign(self, token: str) -> float:
        # a second, independent hash decides the sign, so hash collisions partially
        # cancel instead of only ever adding -- the standard feature-hashing trick
        digest = hashlib.sha256(b"sign:" + token.encode("utf-8")).digest()
        return 1.0 if digest[0] & 1 else -1.0

    def _embed_hashing(self, text: str) -> np.ndarray:
        vector = np.zeros(self.embedding_dim, dtype=np.float64)
        for token in TOKEN_PATTERN.findall(text.lower()):
            bucket = self._hash_bucket(token)
            vector[bucket] += self._hash_sign(token)
        return vector

    # ---------- onnx backend ----------

    def _embed_onnx(self, texts: List[str]) -> np.ndarray:
        encoded = self.tokenizer(
            texts, padding=True, truncation=True, max_length=self.max_length,
            return_tensors="np",
        )
        inputs = {k: v for k, v in encoded.items() if k in {i.name for i in self.session.get_inputs()}}
        outputs = self.session.run(None, inputs)
        token_embeddings = outputs[0]                      # (batch, seq_len, hidden)
        mask = encoded["attention_mask"][..., None].astype(np.float64)

        pooling = self.config.get("pooling", "mean")
        if pooling == "cls":
            pooled = token_embeddings[:, 0, :]
        elif pooling == "max":
            masked = np.where(mask > 0, token_embeddings, -np.inf)
            pooled = masked.max(axis=1)
        else:  # mean, the default -- masked so padding tokens do not dilute the average
            summed = (token_embeddings * mask).sum(axis=1)
            counts = np.clip(mask.sum(axis=1), 1e-9, None)
            pooled = summed / counts
        return pooled

    # ---------- entry point ----------

    def embed(self, text_or_segments: Union[str, List[str]]) -> np.ndarray:
        """One string in -> one (embedding_dim,) vector out. A list in -> a
        (len(list), embedding_dim) matrix, one row per segment, same order."""
        single = isinstance(text_or_segments, str)
        texts = [text_or_segments] if single else list(text_or_segments)

        if self.backend == "onnx":
            matrix = self._embed_onnx(texts)
        else:
            matrix = np.stack([self._embed_hashing(t) for t in texts])

        matrix = matrix.astype(np.float64)
        if self.normalize:
            matrix = np.stack([_l2_normalize(row) for row in matrix])

        return matrix[0] if single else matrix
