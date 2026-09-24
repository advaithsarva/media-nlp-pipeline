"""Pull and push adapters for every non-file input source `pipeline_v1.yaml` names under
`input.sources`: a REST API, Elasticsearch, S3, Kafka, a web scraper, Redis.

Same division of labour as `input_router.py` and `file_readers.py`: a client's job stops
at "here is the text and whatever metadata came with it" -- turning that into an
`InternalDocument` is one shared helper (`_to_internal_document`), not six copies of the
same six lines. `InputRouter.route_pull_source` is what actually decides which client to
use, based on which `input.sources.*.enabled` flag is set in `pipeline_v1.yaml`.

Every client library here (`requests`, `elasticsearch`, `boto3`, `kafka`, `redis`, `bs4`)
is imported lazily, inside the method that needs it, never at module import time. None of
these are needed for the documented working path -- `.txt` in, JSON out, no network calls
(README.md, Operational Considerations: "no external downloads or network calls at
runtime outside io_adapters/") -- so importing this module must not require them to be
installed. A deployment that only ever reads local files should never have to `pip
install boto3` to get `python src/main.py` running.

Each client exposes the same two methods:

    receive(payload)              one already-in-hand record -> InternalDocument
                                   (a webhook body, one ES hit, one Kafka message, ...)
    fetch(source_config, ...)     go and get records -> Iterable[InternalDocument]
                                   (query the API/index/bucket/topic/site/keyspace)

`receive` is for push mode (something else calls this pipeline); `fetch` is for pull mode
(`InputRouter.route_pull_source` calls this pipeline). Both end at the same conversion.
"""

import time
import unicodedata
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

from core.internal_document import InternalDocument, ProcessingStatus, SourceType
from core.exceptions import NoTextFoundError
from nlp_pipeline.deterministic_utils import _hash_to_document_id


def _to_internal_document(text: str, source_type: SourceType,
                          metadata: Optional[Dict[str, Any]] = None,
                          language: str = None, title: str = None,
                          author: str = None) -> InternalDocument:
    """The one place a raw payload becomes the pipeline's single accepted shape.

    Mirrors `InputRouter._to_internal_document`: NFC-normalise once at the boundary
    (everything downstream measures character offsets against this exact string), and
    hash the text itself into the document id so the same article pulled twice -- once
    from an API, once from a scrape -- collapses into one id.
    """
    if not isinstance(text, str) or not text.strip():
        raise NoTextFoundError("ingestion adapter produced no text")
    text = unicodedata.normalize("NFC", text)
    return InternalDocument(
        document_id=_hash_to_document_id(text),
        text=text,
        source_type=source_type,
        ingestion_timestamp=datetime.now(timezone.utc).isoformat(),
        source_metadata=metadata or {},
        language=language,
        title=title,
        author=author,
        processing_status=ProcessingStatus.INGESTED,
    )


def _field(record: Dict[str, Any], field_path: str) -> Any:
    """`"a.b.c"` -> record["a"]["b"]["c"], returning None on any missing/mismatched step
    rather than raising -- a pull source's records rarely all share one exact shape."""
    value: Any = record
    for part in field_path.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


class APIClient:
    """A REST (or GraphQL, same shape) JSON endpoint."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

    def receive(self, json_payload: Dict[str, Any]) -> InternalDocument:
        text_field = self.config.get("text_field", "content")
        text = _field(json_payload, text_field)
        return _to_internal_document(
            text, SourceType.API_REST,
            metadata={k: v for k, v in json_payload.items() if k != text_field},
            language=json_payload.get("language"),
            title=json_payload.get("title"),
            author=json_payload.get("author"),
        )

    def fetch(self, request_config: Dict[str, Any] = None) -> Iterable[InternalDocument]:
        import requests
        cfg = {**self.config, **(request_config or {})}
        response = requests.request(
            method=cfg.get("method", "GET"),
            url=cfg["endpoint"],
            headers=cfg.get("headers"),
            timeout=cfg.get("timeout", 30),
        )
        response.raise_for_status()
        payload = response.json()
        # tolerate either a bare list or {"results": [...]} / {"items": [...]} / {"data": [...]}
        records = payload if isinstance(payload, list) else (
            payload.get("results") or payload.get("items") or payload.get("data") or [payload]
        )
        for record in records[: cfg.get("batch_size", len(records))]:
            yield self.receive(record)


class ESClient:
    """Elasticsearch, via a `query`/`match_all` search rather than a raw scroll id, so
    the same config is reusable across runs without carrying scroll state."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self._client = None

    def _es(self):
        if self._client is None:
            from elasticsearch import Elasticsearch
            self._client = Elasticsearch(
                f"http://{self.config.get('host', 'localhost')}:{self.config.get('port', 9200)}"
            )
        return self._client

    def receive(self, hit_dict: Dict[str, Any]) -> InternalDocument:
        source = hit_dict.get("_source", hit_dict)
        text_field = self.config.get("text_field", "content")
        text = _field(source, text_field)
        metadata = {k: v for k, v in source.items() if k != text_field}
        metadata["_id"] = hit_dict.get("_id")
        metadata["_index"] = hit_dict.get("_index")
        return _to_internal_document(
            text, SourceType.ELASTICSEARCH, metadata=metadata,
            language=source.get("language"), title=source.get("title"), author=source.get("author"),
        )

    def fetch(self, query_config: Dict[str, Any] = None) -> Iterable[InternalDocument]:
        cfg = {**self.config, **(query_config or {})}
        response = self._es().search(
            index=cfg["index"], query=cfg.get("query", {"match_all": {}}),
            size=cfg.get("batch_size", 100),
        )
        for hit in response["hits"]["hits"]:
            yield self.receive(hit)


class S3Client:
    """S3 objects, whether named individually (an S3 event notification) or discovered
    under a prefix."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self._client = None

    def _s3(self):
        if self._client is None:
            import boto3
            self._client = boto3.client(
                "s3", region_name=self.config.get("region"),
                aws_access_key_id=self.config.get("access_key"),
                aws_secret_access_key=self.config.get("secret_key"),
            )
        return self._client

    def _read_object(self, bucket: str, key: str) -> InternalDocument:
        body = self._s3().get_object(Bucket=bucket, Key=key)["Body"].read()
        text = body.decode("utf-8", errors="replace")
        return _to_internal_document(
            text, SourceType.S3, metadata={"bucket": bucket, "key": key}, title=key,
        )

    def receive(self, s3_event: Dict[str, Any]) -> InternalDocument:
        """One record from an S3 "ObjectCreated" event notification."""
        record = s3_event["Records"][0]["s3"]
        return self._read_object(record["bucket"]["name"], record["object"]["key"])

    def fetch(self, s3_config: Dict[str, Any] = None, _ignored=None) -> Iterable[InternalDocument]:
        cfg = {**self.config, **(s3_config or {})}
        bucket = cfg["bucket"]
        paginator = self._s3().get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=bucket, Prefix=cfg.get("prefix", "")):
            for obj in page.get("Contents", []):
                if obj["Key"].endswith("/"):     # a "folder" marker, not a document
                    continue
                yield self._read_object(bucket, obj["Key"])


class KafkaClient:
    """A Kafka topic. `fetch` is bounded (`max_messages` / `poll_timeout_ms`), because an
    unbounded live consumer is not something an `Iterable[InternalDocument]` return type
    can represent -- callers that want a genuinely continuous stream should iterate the
    underlying `KafkaConsumer` directly."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

    def receive(self, message: Dict[str, Any]) -> InternalDocument:
        text_field = self.config.get("text_field", "message")
        text = _field(message, text_field)
        return _to_internal_document(
            text, SourceType.KAFKA,
            metadata={k: v for k, v in message.items() if k != text_field},
        )

    def fetch(self, consumer_config: Dict[str, Any] = None, _ignored=None) -> Iterable[InternalDocument]:
        from kafka import KafkaConsumer
        import json as _json
        cfg = {**self.config, **(consumer_config or {})}
        consumer = KafkaConsumer(
            cfg["topic"],
            bootstrap_servers=cfg.get("bootstrap_servers", "localhost:9092"),
            group_id=cfg.get("group_id", "nlp-pipeline"),
            auto_offset_reset=cfg.get("auto_offset_reset", "earliest"),
            consumer_timeout_ms=cfg.get("poll_timeout_ms", 5000),
            value_deserializer=lambda raw: _json.loads(raw.decode("utf-8")),
        )
        max_messages = cfg.get("max_messages")
        count = 0
        try:
            for record in consumer:
                if max_messages is not None and count >= max_messages:
                    break
                yield self.receive(record.value)
                count += 1
        finally:
            consumer.close()


class ScraperClient:
    """A configured list of URLs, fetched and reduced to their article body with a CSS
    selector. Rate-limited client-side (`rate_limit`, requests per second) -- this
    pipeline does not control the site it is reading, so it has to be the polite party."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

    def receive(self, html_content: Dict[str, Any]) -> InternalDocument:
        """`html_content` is `{"html": "<...>", "url": "...", "css_selector": "..." }`."""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content["html"], "html.parser")
        selector = html_content.get("css_selector") or self.config.get("css_selector")
        nodes = soup.select(selector) if selector else [soup]
        text = "\n\n".join(node.get_text(" ", strip=True) for node in nodes if node.get_text(strip=True))
        title_tag = soup.find("title")
        return _to_internal_document(
            text, SourceType.WEB_SCRAPER,
            metadata={"url": html_content.get("url")},
            title=title_tag.get_text(strip=True) if title_tag else None,
        )

    def fetch(self, urls_config: Dict[str, Any] = None) -> Iterable[InternalDocument]:
        import requests
        cfg = {**self.config, **(urls_config or {})}
        delay = 1.0 / cfg.get("rate_limit", 1) if cfg.get("rate_limit", 1) else 0
        headers = {"User-Agent": cfg.get("user_agent", "NLP-Pipeline/1.0")}

        for i, url in enumerate(cfg.get("urls", [])):
            if i > 0 and delay:
                time.sleep(delay)
            response = requests.get(url, headers=headers, timeout=cfg.get("timeout", 30))
            response.raise_for_status()
            yield self.receive({
                "html": response.text, "url": url, "css_selector": cfg.get("css_selector"),
            })


class RedisClient:
    """Keys matching `key_pattern`, each holding a JSON document (or a bare string)."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self._client = None

    def _redis(self):
        if self._client is None:
            import redis
            self._client = redis.Redis(
                host=self.config.get("host", "localhost"), port=self.config.get("port", 6379),
                db=self.config.get("db", 0), decode_responses=True,
            )
        return self._client

    def receive(self, key_value: Dict[str, Any]) -> InternalDocument:
        """`key_value` is `{"key": "...", "value": "..." or {...}}`."""
        value = key_value["value"]
        if isinstance(value, dict):
            text_field = self.config.get("text_field", "content")
            text = _field(value, text_field)
            metadata = {k: v for k, v in value.items() if k != text_field}
        else:
            text = value
            metadata = {}
        metadata["redis_key"] = key_value.get("key")
        source = value if isinstance(value, dict) else {}
        return _to_internal_document(
            text, SourceType.DATABASE_NOSQL, metadata=metadata,
            language=source.get("language"), title=source.get("title"), author=source.get("author"),
        )

    def fetch(self, _ignored: Dict[str, Any] = None) -> Iterable[InternalDocument]:
        import json as _json
        client = self._redis()
        pattern = self.config.get("key_pattern", "*")
        for key in client.scan_iter(match=pattern):
            raw = client.get(key)
            if raw is None:
                continue
            try:
                value = _json.loads(raw)
            except (ValueError, TypeError):
                value = raw
            yield self.receive({"key": key, "value": value})
