"""EmbeddingGenerator (hashing fallback -- no ONNX model ships with the repo) and
VectorIndex (exact search, faiss or the numpy fallback). Both must be deterministic:
same input, same vector, same ranking, every time -- README.md's "Exact cosine search
(not approximate) preserves reproducibility across runs" is the property under test."""

import numpy as np
import pytest

from nlp_pipeline.embeddings_onnx import EmbeddingGenerator
from nlp_pipeline.vector_index import VectorIndex


@pytest.fixture
def embedder():
    return EmbeddingGenerator({"embedding_dim": 32})


def test_no_model_path_uses_hashing_backend(embedder):
    assert embedder.backend == "hashing"


def test_missing_model_file_falls_back_to_hashing():
    embedder = EmbeddingGenerator({"embedding_dim": 32, "model_path": "models/does_not_exist.onnx"})
    assert embedder.backend == "hashing"


def test_embed_is_deterministic(embedder):
    v1 = embedder.embed("The plan was disastrous and shameful.")
    v2 = embedder.embed("The plan was disastrous and shameful.")
    assert np.array_equal(v1, v2)


def test_embed_shape_and_normalization(embedder):
    vector = embedder.embed("Some article text.")
    assert vector.shape == (32,)
    assert abs(np.linalg.norm(vector) - 1.0) < 1e-9


def test_embed_batch_matches_single(embedder):
    texts = ["first sentence", "second sentence"]
    batch = embedder.embed(texts)
    singles = np.stack([embedder.embed(t) for t in texts])
    assert batch.shape == (2, 32)
    assert np.array_equal(batch, singles)


def test_similar_text_scores_higher_than_unrelated(embedder):
    base = embedder.embed("The election results were announced today.")
    similar = embedder.embed("The election results were announced this morning.")
    unrelated = embedder.embed("A recipe for chocolate chip cookies.")

    assert float(base @ similar) > float(base @ unrelated)


def test_vector_index_search_orders_by_similarity(embedder):
    index = VectorIndex({"embedding_dim": 32})
    a = embedder.embed("cats and dogs are common pets")
    b = embedder.embed("cats and dogs are popular household pets")
    c = embedder.embed("interest rates and monetary policy")

    index.upsert("a", a, {"label": "pets1"})
    index.upsert("b", b, {"label": "pets2"})
    index.upsert("c", c, {"label": "econ"})

    results = index.search(a, top_k=3)
    ids = [r[0] for r in results]
    assert ids[0] == "a"                 # a document is its own best match
    assert ids.index("b") < ids.index("c")


def test_upsert_replaces_existing_id(embedder):
    index = VectorIndex({"embedding_dim": 32})
    v1 = embedder.embed("first version")
    v2 = embedder.embed("second version")

    index.upsert("doc", v1, {"n": 1})
    index.upsert("doc", v2, {"n": 2})

    assert len(index) == 1
    results = index.search(v2, top_k=1)
    assert results[0][0] == "doc"
    assert results[0][2]["n"] == 2


def test_remove_drops_a_vector(embedder):
    index = VectorIndex({"embedding_dim": 32})
    index.upsert("a", embedder.embed("alpha"), {})
    index.upsert("b", embedder.embed("beta"), {})
    index.remove("a")

    assert len(index) == 1
    assert [r[0] for r in index.search(embedder.embed("alpha"), top_k=5)] == ["b"]


def test_search_on_empty_index_returns_empty_list(embedder):
    index = VectorIndex({"embedding_dim": 32})
    assert index.search(embedder.embed("anything"), top_k=5) == []


def test_dimension_mismatch_raises(embedder):
    index = VectorIndex({"embedding_dim": 32})
    with pytest.raises(ValueError):
        index.upsert("a", np.zeros(8), {})


def test_search_is_deterministic_across_runs(embedder):
    index = VectorIndex({"embedding_dim": 32})
    for i in range(10):
        index.upsert(f"doc{i}", embedder.embed(f"document number {i} about topic {i % 3}"), {})

    query = embedder.embed("document about topic 1")
    first = index.search(query, top_k=5)
    second = index.search(query, top_k=5)
    assert first == second
