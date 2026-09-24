"""A vector index for nearest-neighbour search over document/sentence embeddings.

Read-only semantic memory: `EmbeddingGenerator` produces vectors, this stores and
searches them, and nothing in the scoring path treats a nearest-neighbour result as
evidence -- a similarity score cannot be quoted as a substring the way `EvidenceSpan.text`
can, so this stays a side channel (taxonomy suggestions, near-duplicate detection),
not an input to `ScoringEngine`.

Exact search only, never approximate (IVF/HNSW/PQ). README.md's scoring-mathematics
section is explicit about why: "Exact cosine search (not approximate) preserves
reproducibility across runs" -- an approximate index can return a different neighbour
set for the same query depending on build order, which would break the same
same-input-same-output guarantee the rest of the project is built around.

Two backends:

  faiss    `faiss.IndexFlatIP` -- exact inner-product search. With L2-normalised vectors
           (which is what `EmbeddingGenerator` always returns), inner product equals
           cosine similarity, and Flat means brute-force: no clustering, no
           approximation, so results depend only on the data, never on training order.
  numpy    Used when `faiss` is not installed. The identical algorithm -- brute-force
           inner product -- implemented directly over a numpy matrix, so behaviour does
           not change based on whether the optional dependency happens to be present.
"""

from typing import Any, Dict, List, Tuple

import numpy as np

try:
    import faiss
    _HAS_FAISS = True
except ImportError:
    _HAS_FAISS = False


class VectorIndex:
    def __init__(self, index_config: Dict[str, Any] = None):
        self.config = index_config or {}
        self.dim = int(self.config.get("embedding_dim", 384))
        self.backend = "faiss" if (_HAS_FAISS and self.config.get("backend", "faiss") == "faiss") else "numpy"

        self._faiss_index = faiss.IndexFlatIP(self.dim) if self.backend == "faiss" else None
        self._vectors = np.zeros((0, self.dim), dtype=np.float32)

        # Parallel to the vectors: row i's document_id and metadata. faiss stores only
        # numbers, so this is what turns a row index back into something meaningful.
        self._ids: List[str] = []
        self._metadata: List[Dict[str, Any]] = []
        self._id_to_row: Dict[str, int] = {}

    def __len__(self) -> int:
        return len(self._ids)

    # ---------- writes ----------

    def upsert(self, document_id: str, embedding: np.ndarray, metadata: Dict[str, Any] = None):
        """Insert, or replace in place if `document_id` is already indexed.

        faiss has no in-place update or delete for a Flat index, so a replace is done by
        rebuilding the backing index from the (small, in-memory) vector matrix -- fine at
        the scale this project's read-only semantic memory is meant for; a production
        deployment with millions of vectors would want an ids-supporting index instead.
        """
        vector = np.asarray(embedding, dtype=np.float32).reshape(-1)
        if vector.shape[0] != self.dim:
            raise ValueError(f"embedding has dimension {vector.shape[0]}, index expects {self.dim}")

        if document_id in self._id_to_row:
            row = self._id_to_row[document_id]
            self._vectors[row] = vector
            self._metadata[row] = metadata or {}
        else:
            row = len(self._ids)
            self._vectors = np.vstack([self._vectors, vector[None, :]])
            self._ids.append(document_id)
            self._metadata.append(metadata or {})
            self._id_to_row[document_id] = row

        if self.backend == "faiss":
            self._faiss_index = faiss.IndexFlatIP(self.dim)
            if len(self._vectors):
                self._faiss_index.add(self._vectors)

    def remove(self, document_id: str):
        """Drop one vector and rebuild. Same rebuild trade-off as `upsert`."""
        if document_id not in self._id_to_row:
            return
        row = self._id_to_row.pop(document_id)
        self._ids.pop(row)
        self._metadata.pop(row)
        self._vectors = np.delete(self._vectors, row, axis=0)
        self._id_to_row = {doc_id: i for i, doc_id in enumerate(self._ids)}
        if self.backend == "faiss":
            self._faiss_index = faiss.IndexFlatIP(self.dim)
            if len(self._vectors):
                self._faiss_index.add(self._vectors)

    # ---------- reads ----------

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[str, float, Dict[str, Any]]]:
        """Nearest neighbours by cosine similarity (inner product on normalised vectors),
        as `[(document_id, score, metadata), ...]`, best match first.

        Ties are broken by document_id so the order is stable regardless of insertion
        order or which backend produced it -- required for the determinism guarantee the
        rest of the pipeline holds itself to.
        """
        if len(self._ids) == 0:
            return []

        query = np.asarray(query_embedding, dtype=np.float32).reshape(1, -1)
        if query.shape[1] != self.dim:
            raise ValueError(f"query has dimension {query.shape[1]}, index expects {self.dim}")

        k = min(max(top_k, 0), len(self._ids))
        if k == 0:
            return []

        if self.backend == "faiss":
            scores, indices = self._faiss_index.search(query, k)
            scores, indices = scores[0], indices[0]
        else:
            all_scores = (self._vectors @ query[0])
            order = np.argsort(-all_scores, kind="stable")[:k]
            scores, indices = all_scores[order], order

        results = [
            (self._ids[i], float(scores[pos]), self._metadata[i])
            for pos, i in enumerate(indices) if i != -1
        ]
        # stable, deterministic tie-break: score descending, then document_id ascending
        results.sort(key=lambda r: (-round(r[1], 9), r[0]))
        return results[:k]
