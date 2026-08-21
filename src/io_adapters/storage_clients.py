"""Writes finished analysis records somewhere durable.

Everything here takes a plain dict -- the record `PostProcessor` produced -- and puts it
somewhere. No writer is allowed to change the record on its way past; if a writer had to
reshape the data, two storage backends would end up holding different answers to the same
question.

JSONL is the default and needs nothing beyond the standard library. Parquet is worth it
once there are enough records that you want columns rather than lines, and it pulls in
pyarrow, so that import happens inside the writer rather than at the top of the file.
"""

import json
from pathlib import Path
from typing import Dict, Any, List


class JSONLWriter:
    """One JSON object per line. Append-friendly, greppable, readable in a text editor."""

    def __init__(self, config: Dict[str, Any] = None):
        config = config or {}
        self.path = Path(config.get("path", "data/processed")) / config.get("file", "records.jsonl")
        self.encoding = config.get("jsonl", {}).get("encoding", "utf-8")
        # append=False means each run starts a fresh file
        self.append = config.get("jsonl", {}).get("append", False)
        self._started = False

    def write(self, record: Dict[str, Any]):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # the first write of a run truncates unless append was asked for; later writes
        # in the same run always append, otherwise the file would only ever hold one record
        mode = "a" if (self.append or self._started) else "w"
        self._started = True
        with open(self.path, mode, encoding=self.encoding) as f:
            # sort_keys for the same reason as everywhere else: the same record must
            # serialise to the same bytes every time
            f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
        return str(self.path)

    def save_batch(self, records: List[Dict[str, Any]]):
        for record in records:
            self.write(record)
        return str(self.path)


class JSONWriter:
    """One file per document, named by document id. Handy while developing."""

    def __init__(self, config: Dict[str, Any] = None):
        config = config or {}
        self.folder = Path(config.get("path", "data/processed"))

    def write(self, record: Dict[str, Any]):
        self.folder.mkdir(parents=True, exist_ok=True)
        # the first 16 characters of the hash are plenty to tell documents apart and
        # keep the filename readable
        target = self.folder / (record["document_id"][:16] + ".json")
        target.write_text(
            json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return str(target)

    def save_batch(self, records: List[Dict[str, Any]]):
        return [self.write(record) for record in records]


class ParquetWriter:
    """Columnar storage. Worth using once you have thousands of records to query."""

    def __init__(self, config: Dict[str, Any] = None):
        config = config or {}
        self.path = Path(config.get("path", "data/processed")) / config.get("file", "records.parquet")
        self.compression = config.get("parquet", {}).get("compression", "snappy")

    def _flatten(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Parquet columns hold scalars, so the nested parts are stored as JSON strings.

        Losing the nesting sounds bad, but the alternative -- one row per finding -- makes
        the document-level scores repeat on every row. The JSON strings can be parsed back
        by whoever reads the file.
        """
        return {
            "document_id": record["document_id"],
            "schema_version": record["schema_version"],
            "source_type": record["source"]["type"],
            "title": record["source"]["title"],
            "language": record["source"]["language"],
            "char_count": record["stats"]["char_count"],
            "word_count": record["stats"]["word_count"],
            "sentence_count": record["stats"]["sentence_count"],
            "finding_count": len(record["findings"]),
            "findings_json": json.dumps(record["findings"], sort_keys=True),
            "category_scores_json": json.dumps(record["category_scores"], sort_keys=True),
            "config_hashes_json": json.dumps(record["config_hashes"], sort_keys=True),
            "composite": record["composite"],
        }

    def save_batch(self, records: List[Dict[str, Any]]):
        # imported here, not at the top: pyarrow is a large dependency and nothing else
        # in the pipeline needs it
        import pyarrow as pa
        import pyarrow.parquet as pq

        self.path.parent.mkdir(parents=True, exist_ok=True)
        table = pa.Table.from_pylist([self._flatten(r) for r in records])
        pq.write_table(table, self.path, compression=self.compression)
        return str(self.path)

    def write(self, record: Dict[str, Any]):
        # Parquet writes whole files, not lines. A single record still means rewriting
        # the file, which is why this format is for batches.
        return self.save_batch([record])


class StorageClientFactory:
    """Turns the `output.type` string in pipeline_v1.yaml into the matching writer."""

    WRITERS = {
        "jsonl": JSONLWriter,
        "json": JSONWriter,
        "parquet": ParquetWriter,
    }

    @classmethod
    def create(cls, output_config: Dict[str, Any]):
        output_config = output_config or {}
        kind = output_config.get("type", "jsonl")
        if kind not in cls.WRITERS:
            known = ", ".join(sorted(cls.WRITERS))
            raise ValueError("unknown output type " + repr(kind) + ". Known: " + known)
        return cls.WRITERS[kind](output_config)
