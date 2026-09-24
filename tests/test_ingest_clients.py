"""Every non-file ingestion adapter's `receive()` -- the push-mode conversion that needs
no live network, database, queue, or website. `fetch()` (pull mode) does real I/O with
an external client library and is exercised in the docstring examples / at deploy time,
not here -- there is nothing this suite could assert about a real Kafka broker or S3
bucket without turning "pytest" into an integration harness.
"""

import pytest

from core.internal_document import SourceType
from io_adapters.ingest_clients import (
    APIClient, ESClient, KafkaClient, RedisClient, S3Client, ScraperClient,
)
from core.exceptions import NoTextFoundError


def test_api_client_receive():
    client = APIClient({"text_field": "content"})
    doc = client.receive({"content": "Some article body.", "title": "T", "author": "A", "language": "en"})

    assert doc.text == "Some article body."
    assert doc.source_type == SourceType.API_REST
    assert doc.title == "T"
    assert doc.author == "A"
    assert doc.language == "en"
    assert "content" not in doc.source_metadata


def test_api_client_missing_text_field_raises():
    client = APIClient({"text_field": "content"})
    with pytest.raises(NoTextFoundError):
        client.receive({"title": "no content field here"})


def test_es_client_receive_reads_from_source():
    client = ESClient({"text_field": "body"})
    hit = {"_id": "42", "_index": "news", "_source": {"body": "Article text.", "title": "T"}}
    doc = client.receive(hit)

    assert doc.text == "Article text."
    assert doc.source_type == SourceType.ELASTICSEARCH
    assert doc.source_metadata["_id"] == "42"
    assert doc.source_metadata["_index"] == "news"
    assert "body" not in doc.source_metadata


def test_kafka_client_receive_uses_configured_field():
    client = KafkaClient({"text_field": "message"})
    doc = client.receive({"message": "Kafka payload text.", "offset": 7})

    assert doc.text == "Kafka payload text."
    assert doc.source_type == SourceType.KAFKA
    assert doc.source_metadata["offset"] == 7


def test_redis_client_receive_with_dict_value():
    client = RedisClient({"text_field": "content"})
    doc = client.receive({"key": "nlp:input:1", "value": {"content": "Redis text.", "author": "bob"}})

    assert doc.text == "Redis text."
    assert doc.author == "bob"
    assert doc.source_metadata["redis_key"] == "nlp:input:1"


def test_redis_client_receive_with_plain_string_value():
    client = RedisClient({})
    doc = client.receive({"key": "k1", "value": "Just a plain string value."})

    assert doc.text == "Just a plain string value."
    assert doc.source_metadata["redis_key"] == "k1"


def test_scraper_client_receive_applies_css_selector():
    client = ScraperClient({})
    html = (
        "<html><head><title>Headline</title></head>"
        "<body><nav>skip this</nav><div class='article'>Real article text.</div></body></html>"
    )
    doc = client.receive({"html": html, "url": "http://example.test/a", "css_selector": ".article"})

    assert doc.text == "Real article text."
    assert doc.title == "Headline"
    assert doc.source_metadata["url"] == "http://example.test/a"


def test_scraper_client_receive_without_selector_uses_whole_page():
    client = ScraperClient({})
    html = "<html><body><p>Only paragraph.</p></body></html>"
    doc = client.receive({"html": html, "url": "http://example.test/b"})
    assert "Only paragraph." in doc.text


def test_s3_client_receive_parses_event_notification(monkeypatch):
    client = S3Client({})

    class FakeBody:
        def read(self):
            return b"S3 object text content."

    class FakeS3:
        def get_object(self, Bucket, Key):
            assert Bucket == "my-bucket"
            assert Key == "raw/doc1.txt"
            return {"Body": FakeBody()}

    monkeypatch.setattr(client, "_s3", lambda: FakeS3())

    event = {"Records": [{"s3": {"bucket": {"name": "my-bucket"}, "object": {"key": "raw/doc1.txt"}}}]}
    doc = client.receive(event)

    assert doc.text == "S3 object text content."
    assert doc.source_type == SourceType.S3
    assert doc.source_metadata == {"bucket": "my-bucket", "key": "raw/doc1.txt"}


def test_two_identical_texts_from_different_sources_collapse_to_one_document_id():
    """The whole point of hashing the text itself (see input_router.py's own version of
    this): the same article pulled twice, from two different adapters, is one document."""
    api_doc = APIClient({"text_field": "content"}).receive({"content": "Same text everywhere."})
    kafka_doc = KafkaClient({"text_field": "message"}).receive({"message": "Same text everywhere."})
    assert api_doc.document_id == kafka_doc.document_id


def test_input_router_never_pulls_a_disabled_source():
    from io_adapters.input_router import InputRouter

    router = InputRouter({"sources": {"files": {"enabled": False}, "api": {"enabled": False}}})
    assert list(router.route_pull_source()) == []


def test_input_router_dispatches_to_enabled_non_file_source(monkeypatch):
    from io_adapters import input_router

    calls = []

    class FakeClient:
        def __init__(self, config):
            self.config = config

        def fetch(self, source_config):
            calls.append(source_config)
            return iter([APIClient({"text_field": "content"}).receive({"content": "from fake api"})])

    monkeypatch.setitem(input_router.PULL_CLIENTS, "api", FakeClient)
    router = input_router.InputRouter({"sources": {
        "files": {"enabled": False},
        "api": {"enabled": True, "endpoint": "http://example.test"},
    }})

    documents = list(router.route_pull_source())

    assert len(documents) == 1
    assert documents[0].text == "from fake api"
    assert calls == [{"enabled": True, "endpoint": "http://example.test"}]
