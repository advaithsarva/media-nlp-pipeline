"""The HTTP contract. Same pipeline, same guarantees, reached over the network."""

import pytest

fastapi_testclient = pytest.importorskip("fastapi.testclient")

from conftest import LOADED_TEXT, NEUTRAL_TEXT      # noqa: E402
from api.service import create_app                  # noqa: E402


@pytest.fixture(scope="module")
def client():
    return fastapi_testclient.TestClient(create_app())


def test_health_reports_the_taxonomy(client):
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "loaded_language" in body["categories"]
    assert len(body["config_hashes"]["taxonomy_hash"]) == 64


def test_analyze_returns_findings_with_real_offsets(client):
    response = client.post("/analyze", json={"text": LOADED_TEXT})

    assert response.status_code == 200
    body = response.json()
    assert body["findings"]
    for finding in body["findings"]:
        assert LOADED_TEXT[finding["start_char"]:finding["end_char"]] == finding["text"]


def test_neutral_text_returns_an_empty_report(client):
    response = client.post("/analyze", json={"text": NEUTRAL_TEXT})

    assert response.status_code == 200
    assert response.json()["findings"] == []


def test_same_request_twice_gives_the_same_answer(client):
    first = client.post("/analyze", json={"text": LOADED_TEXT}).json()
    second = client.post("/analyze", json={"text": LOADED_TEXT}).json()

    assert first == second


def test_empty_text_is_rejected_before_the_pipeline(client):
    response = client.post("/analyze", json={"text": ""})

    assert response.status_code == 422      # pydantic rejects it, not the pipeline


def test_missing_text_is_rejected(client):
    response = client.post("/analyze", json={"title": "no body"})

    assert response.status_code == 422


def test_batch_handles_several_documents(client):
    response = client.post("/analyze/batch", json={
        "documents": [{"text": LOADED_TEXT}, {"text": NEUTRAL_TEXT}],
    })

    assert response.status_code == 200
    results = response.json()["results"]
    assert len(results) == 2
    assert results[0]["findings"] and results[1]["findings"] == []


def test_empty_batch_is_rejected(client):
    response = client.post("/analyze/batch", json={"documents": []})

    assert response.status_code == 400


def test_no_composite_over_http(client):
    body = client.post("/analyze", json={"text": LOADED_TEXT}).json()

    assert body["composite"] is None
    assert all(not score["calibrated"] for score in body["category_scores"].values())
