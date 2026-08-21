"""The single door into the pipeline.

Anything can arrive here -- a file path, a string of text, a dict from an API. Whatever
it is, it leaves as one InternalDocument, and that is the only shape the NLP stages ever
see. Nothing downstream knows or cares whether the article came from a PDF or a POST.

Division of labour, which the previous version got wrong: the readers in file_readers.py
return plain dictionaries of everything they could find in a file. Only
_to_internal_document turns one of those dictionaries into an InternalDocument. Readers
never build documents; the router never parses files.
"""

import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Iterator, Optional

from core.internal_document import InternalDocument, SourceType, ProcessingStatus
from core.exceptions import (
    UnsupportedFileTypeError,
    NoTextFoundError,
    InvalidInputError,
)
from nlp_pipeline.deterministic_utils import _hash_to_document_id
from io_adapters.file_readers import (
    TxtReader,
    PDFReader,
    DocsReader,
    CSVReader,
    JSONReader,
    JSONLReader,
    HTMLReader,
    XMLReader,
    MarkdownReader,
)

# extension -> (reader class, what to record as the source type)
EXTENSION_MAP = {
    ".txt":      (TxtReader,      SourceType.FILE_TXT),
    ".md":       (MarkdownReader, SourceType.FILE_MARKDOWN),
    ".markdown": (MarkdownReader, SourceType.FILE_MARKDOWN),
    ".pdf":      (PDFReader,      SourceType.FILE_PDF),
    ".docx":     (DocsReader,     SourceType.FILE_DOCX),
    ".csv":      (CSVReader,      SourceType.FILE_CSV),
    ".tsv":      (CSVReader,      SourceType.FILE_CSV),
    ".json":     (JSONReader,     SourceType.FILE_JSON),
    ".jsonl":    (JSONLReader,    SourceType.FILE_JSONL),
    ".html":     (HTMLReader,     SourceType.FILE_HTML),
    ".htm":      (HTMLReader,     SourceType.FILE_HTML),
    ".xml":      (XMLReader,      SourceType.FILE_XML),
}

# Where each reader puts the text it extracted, best first. The readers disagree because
# they were written separately; this list is the one place that difference is absorbed.
TEXT_KEYS = ("raw_content", "full_raw_text", "extracted_text", "plain_text", "text", "content")


class InputRouter:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.file_config = self.config.get("sources", {}).get("files", {})
        # One instance per reader class, made once and reused. The old version stored the
        # string "TxtReader()" here, which is why no reader was ever actually called.
        self.readers = {}
        for extension, (reader_class, _) in EXTENSION_MAP.items():
            if reader_class not in self.readers:
                self.readers[reader_class] = reader_class()

    # ---------- entry points ----------

    def route_push_input(self, payload, source_hint: str = "") -> InternalDocument:
        """Something was handed to us. Work out what it is and convert it."""
        if isinstance(payload, InternalDocument):
            return payload
        if isinstance(payload, Path):
            return self._handle_file_path(payload)
        if isinstance(payload, bytes):
            return self._handle_raw_text(payload.decode("utf-8", errors="replace"), source_hint)
        if isinstance(payload, dict):
            return self._handle_payload(payload, source_hint)
        if isinstance(payload, str):
            # a path only if it actually exists -- otherwise it is just text that
            # happens to look like one
            candidate = Path(payload)
            if len(payload) < 260 and candidate.is_file():
                return self._handle_file_path(candidate)
            return self._handle_raw_text(payload, source_hint)
        raise InvalidInputError("cannot route input of type " + type(payload).__name__)

    def route_pull_source(self) -> Iterator[InternalDocument]:
        """Go and fetch. Only the local-files source is wired up; the rest are off in config."""
        if not self.file_config.get("enabled", False):
            return
        directory = self.file_config.get("path", "data/raw")
        pattern = self.file_config.get("glob_pattern", "*.txt")
        for document in self.process_directory(directory, pattern):
            yield document

    def process_directory(self, directory, pattern: str = "*.txt") -> Iterator[InternalDocument]:
        folder = Path(directory)
        if not folder.is_dir():
            raise InvalidInputError("not a directory: " + str(folder))
        # sorted, because the order the filesystem hands back files is not stable and
        # the pipeline promises the same output every run
        for path in sorted(folder.glob(pattern)):
            if path.is_file():
                yield self._handle_file_path(path)

    # ---------- one input at a time ----------

    def _handle_file_path(self, file_path) -> InternalDocument:
        path = Path(file_path)
        if not path.is_file():
            raise InvalidInputError("file not found: " + str(path))

        extension = path.suffix.lower()
        if extension not in EXTENSION_MAP:
            known = ", ".join(sorted(EXTENSION_MAP))
            raise UnsupportedFileTypeError("no reader for " + extension + ". Known: " + known)

        reader_class, source_type = EXTENSION_MAP[extension]
        raw_record = self.readers[reader_class].read(str(path))
        return self._to_internal_document(raw_record, source_type)

    def _handle_raw_text(self, text: str, source_hint: str = "") -> InternalDocument:
        raw_record = {"raw_content": text, "source_hint": source_hint}
        return self._to_internal_document(raw_record, SourceType.API_REST)

    def _handle_payload(self, payload: Dict[str, Any], source_hint: str = "") -> InternalDocument:
        source_type = SourceType.API_REST
        if payload.get("source_type"):
            try:
                source_type = SourceType(payload["source_type"])
            except ValueError:
                pass    # an unknown label is not worth failing the whole document over
        return self._to_internal_document(dict(payload), source_type)

    # ---------- the conversion itself ----------

    def _extract_text(self, raw_record: Dict[str, Any]) -> str:
        for key in TEXT_KEYS:
            value = raw_record.get(key)
            if isinstance(value, str) and value.strip():
                return value

        # Tabular and record-shaped files: the config says which column or field holds
        # the article, because guessing would be a silent data bug.
        rows = raw_record.get("raw_data") or raw_record.get("all_records")
        if isinstance(rows, list) and rows:
            column = self._configured_text_key()
            pieces = []
            for row in rows:
                cell = self._cell_from_row(row, column)
                if isinstance(cell, str) and cell.strip():
                    pieces.append(cell)
            if pieces:
                return "\n\n".join(pieces)

        parsed = raw_record.get("parsed_json")
        if isinstance(parsed, dict):
            value = parsed.get(self._configured_text_key())
            if isinstance(value, str) and value.strip():
                return value

        name = raw_record.get("file_name", "input")
        raise NoTextFoundError("no text found in record from " + str(name))

    def _configured_text_key(self) -> str:
        csv_column = self.file_config.get("csv", {}).get("text_column")
        json_field = self.file_config.get("json", {}).get("text_field")
        return csv_column or json_field or "content"

    def _cell_from_row(self, row, column):
        """JSONL wraps each line as {'line_number': n, 'data': {...}}; CSV rows are flat."""
        if not isinstance(row, dict):
            return None
        if column in row:
            return row[column]
        inner = row.get("data")
        if isinstance(inner, dict):
            return inner.get(column)
        return None

    def _to_internal_document(self, raw_record: Dict[str, Any],
                              source_type: SourceType) -> InternalDocument:
        text = self._extract_text(raw_record)
        # NFC once, here at the boundary. Every character offset the pipeline ever
        # reports is measured against this exact string.
        text = unicodedata.normalize("NFC", text)

        # The id is a hash of the text itself, so the same article gets the same id on
        # any machine, with no database and no counter. Two identical articles collapse
        # into one document -- good for deduplication, and deliberate.
        document_id = _hash_to_document_id(text)

        metadata = {}
        for key, value in raw_record.items():
            if key not in TEXT_KEYS:
                metadata[key] = value

        return InternalDocument(
            document_id=document_id,
            text=text,
            source_type=source_type,
            ingestion_timestamp=datetime.now(timezone.utc).isoformat(),
            source_metadata=metadata,
            language=raw_record.get("language"),
            title=raw_record.get("title") or raw_record.get("file_name"),
            author=raw_record.get("author"),
            processing_status=ProcessingStatus.INGESTED,
        )
