"""Writers must store the record unchanged, and the factory must respect the config."""

import json

import pytest

from io_adapters.storage_clients import (
    JSONLWriter,
    JSONWriter,
    ParquetWriter,
    StorageClientFactory,
)

RECORD = {
    "schema_version": "1.0.0",
    "document_id": "a" * 64,
    "source": {"type": "file_txt", "title": "t", "author": None, "language": "en"},
    "config_hashes": {"pipeline_hash": "b" * 64, "taxonomy_hash": "c" * 64, "scoring_hash": "d" * 64},
    "stats": {"char_count": 10, "word_count": 2, "sentence_count": 1},
    "findings": [{"category": "loaded_language", "rule_id": "loaded_language:lexicon",
                  "sentence_id": 0, "text": "vile", "start_char": 0, "end_char": 4,
                  "confidence": 0.85}],
    "category_scores": {"loaded_language": {"count": 1, "raw": 0.85, "score": 0.5,
                                            "calibrated": False}},
    "composite": None,
    "notes": [],
}


def test_jsonl_round_trips_the_record_unchanged(tmp_path):
    writer = JSONLWriter({"path": str(tmp_path), "file": "out.jsonl"})
    writer.write(RECORD)

    line = (tmp_path / "out.jsonl").read_text(encoding="utf-8").strip()
    assert json.loads(line) == RECORD


def test_jsonl_appends_within_one_run(tmp_path):
    writer = JSONLWriter({"path": str(tmp_path), "file": "out.jsonl"})
    writer.save_batch([RECORD, RECORD, RECORD])

    lines = (tmp_path / "out.jsonl").read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 3


def test_jsonl_starts_fresh_on_a_new_run(tmp_path):
    JSONLWriter({"path": str(tmp_path), "file": "out.jsonl"}).save_batch([RECORD, RECORD])
    JSONLWriter({"path": str(tmp_path), "file": "out.jsonl"}).write(RECORD)

    lines = (tmp_path / "out.jsonl").read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 1


def test_json_writes_one_file_named_by_document(tmp_path):
    target = JSONWriter({"path": str(tmp_path)}).write(RECORD)

    assert target.endswith("aaaaaaaaaaaaaaaa.json")
    assert json.loads(open(target, encoding="utf-8").read()) == RECORD


def test_writing_twice_produces_identical_bytes(tmp_path):
    first = tmp_path / "one"
    second = tmp_path / "two"
    JSONLWriter({"path": str(first), "file": "o.jsonl"}).write(RECORD)
    JSONLWriter({"path": str(second), "file": "o.jsonl"}).write(RECORD)

    assert (first / "o.jsonl").read_bytes() == (second / "o.jsonl").read_bytes()


def test_factory_picks_the_writer_named_in_config():
    assert isinstance(StorageClientFactory.create({"type": "jsonl"}), JSONLWriter)
    assert isinstance(StorageClientFactory.create({"type": "json"}), JSONWriter)
    assert isinstance(StorageClientFactory.create({"type": "parquet"}), ParquetWriter)


def test_factory_defaults_to_jsonl():
    assert isinstance(StorageClientFactory.create({}), JSONLWriter)


def test_factory_refuses_an_unknown_type():
    with pytest.raises(ValueError):
        StorageClientFactory.create({"type": "carrier-pigeon"})


def test_parquet_flattening_keeps_everything():
    """pyarrow may not be installed; the flattening step can still be checked."""
    flat = ParquetWriter()._flatten(RECORD)

    assert flat["document_id"] == RECORD["document_id"]
    assert flat["finding_count"] == 1
    assert json.loads(flat["findings_json"]) == RECORD["findings"]
    assert json.loads(flat["category_scores_json"]) == RECORD["category_scores"]
