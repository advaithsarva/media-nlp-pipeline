# `io_adapters/input_router.py` — rewrite spec

Status: **spec only.** `src/io_adapters/input_router.py` (595 lines, ChatGPT-generated) stays in
place as reference until this rewrite passes its tests — R12.

Target: ~130 lines. Phase 0 item 2.

---

## 1. Why the current file cannot run

| Line | Problem |
|---|---|
| 26 | Imports `UnsupportedInputError` from `core.exceptions`. That class does not exist — there are six classes there and this is not one of them. `import input_router` raises `ImportError`. Nothing downstream runs. |
| 575 | Calls `self.route_push_input(...)` but the method is defined as `_route_push_input` (line 126). `AttributeError` the moment `_process_directory` executes. |
| 99–109 | Registers `ParquetReader`, `ImageReader`, `ArchiveReader`, `AudioReader`. All four are `class X: def __init__(self): pass` with **no `read()` method**. Routing to them produces `AttributeError`, not a clean `UnsupportedFileTypeError`. |
| 248 | `raw_record = self._mock_file_read(...)`. The real call sits commented out on line 245. This is the bug that blocks Phase 0. |
| 33–38 | Imports `APIClient`, `ESClient`, `KafkaClient`, `S3Client` — all R7-frozen stubs. |

## 2. What the rewrite deletes, and why

| Cut | Reason |
|---|---|
| `_route_pull_source`, `_fetch_from_source`, `_initialize_source_clients`, the `ingest_clients` import | Every client is R7-frozen. `_fetch_from_source` literally does `return iter([])` — the entire pull path is a 40-line no-op. |
| `_handle_api_payload`, `_handle_es_hit`, `_handle_kafka_message` | Push handlers for sources that do not exist yet. |
| `_extract_text_from_payload` | Only those three handlers called it. |
| `_mock_file_read` | Replaced by the real reader call. |
| `_handle_file_bytes` | No caller. Comes back when the FastAPI service exists (Phase 1). |
| `_determine_source_type` (20-branch if/elif) | The extension is already known at the call site. A dict lookup replaces the whole chain. |
| `_generate_document_id` | `deterministic_utils._hash_to_document_id` is the same sha256. Two hashers in one repo eventually give two different answers. |

## 3. Two decisions to make before typing

**D1 — `datetime.now()` vs. byte-identical reruns.**
Phase 0's done-criterion is "two consecutive runs are byte-identical". `ingestion_timestamp`
set from `now()` breaks that by construction.

- (a) accept it, and have `test_determinism` compare output with that field excluded
- (b) use the file's `modified_timestamp`, which is stable for the same file

**(b) is recommended** — the timestamp then describes the document rather than the run. The
pseudocode below leans on the reader's `processed_timestamp`; swap it if you pick (a).

**D2 — `_extract_text` last resort.**
The current code, on finding no text field, does `json.dumps(raw_record)` and returns it **as
the article text**. JSON braces and file paths then flow into the NLP pipeline and evidence
spans point at metadata. The spec below raises `NoTextFoundError` instead. This is the R4
argument: a wrong span is worse than no document.

---

## 4. Pseudocode

```
# ─────────────────────────────────────────────────────────────
# MODULE: io_adapters/input_router.py
# The ONLY place an InternalDocument is constructed. Hard rule.
# ─────────────────────────────────────────────────────────────

IMPORT Path, logging, json, datetime
IMPORT the 9 readers that actually have a read() method:
       Txt, Markdown, PDF, Docs, CSV, JSON, JSONL, HTML, XML
IMPORT InternalDocument, SourceType, ProcessingStatus   from core.internal_document
IMPORT IngestionError, UnsupportedFileTypeError,
       NoTextFoundError, InvalidInputError               from core.exceptions
IMPORT _hash_to_document_id                              from nlp_pipeline.deterministic_utils


# One table, two jobs: which reader opens the file, and what SourceType the
# document is stamped with. Keeping both in one place means adding a format
# is one new row, not two edits in two different methods.
CONSTANT EXTENSION_TABLE = {
    ".txt"   -> (TxtReader,      SourceType.FILE_TXT),
    ".text"  -> (TxtReader,      SourceType.FILE_TXT),
    ".md"    -> (MarkdownReader, SourceType.FILE_MARKDOWN),
    ".pdf"   -> (PDFReader,      SourceType.FILE_PDF),
    ".docx"  -> (DocsReader,     SourceType.FILE_DOCX),
    ".csv"   -> (CSVReader,      SourceType.FILE_CSV),
    ".tsv"   -> (CSVReader,      SourceType.FILE_CSV),
    ".json"  -> (JSONReader,     SourceType.FILE_JSON),
    ".jsonl" -> (JSONLReader,    SourceType.FILE_JSONL),
    ".html"  -> (HTMLReader,     SourceType.FILE_HTML),
    ".htm"   -> (HTMLReader,     SourceType.FILE_HTML),
    ".xml"   -> (XMLReader,      SourceType.FILE_XML),
}
# Deliberately NOT listed: .parquet .png .zip .mp3 — their reader classes have
# no read() method. Absent from the table means a clean UnsupportedFileTypeError,
# which is correct. Listing them would give AttributeError instead.


CLASS InputRouter:

    FUNCTION __init__(self, config, output_dir = "./ingestion_output"):
        STORE config
        STORE output_dir as a Path; create it including parents if missing
        CREATE a logger named "InputRouter"

        # Build one reader instance per extension. Readers are stateless so
        # instances can be shared — but each entry must be a real OBJECT,
        # never the string "TxtReader()". That was the original bug.
        self.readers = {}
        FOR EACH (extension, (reader_class, source_type)) IN EXTENSION_TABLE:
            self.readers[extension] = reader_class()      # instantiate ONCE
        # self.readers is now: {".txt": <TxtReader object>, ...}


    # ══ PUBLIC ENTRY POINT ════════════════════════════════════
    # No leading underscore: this is what main.py and process_directory call.
    # (Your convention: underscore marks your internal helpers.)

    FUNCTION route_push_input(self, file_path = None, raw_text = None) -> InternalDocument:

        # Exactly one input must be supplied. Checking at the door turns a
        # confusing failure deep inside a reader into a clear error here.
        IF file_path IS NOT None:
            RETURN self._handle_file_path(file_path)
        ELSE IF raw_text IS NOT None:
            RETURN self._handle_raw_text(raw_text)
        ELSE:
            RAISE InvalidInputError("no input provided: pass file_path or raw_text")

        # NOTE: no try/except wrapper. The original caught Exception and
        # re-raised as IngestionError, discarding the original traceback.
        # Everything raised below is already an IngestionError subclass.


    # ══ FILE PATH → INTERNAL DOCUMENT ═════════════════════════

    FUNCTION _handle_file_path(self, file_path) -> InternalDocument:

        path = Path(file_path)

        IF path does not exist:
            RAISE FileNotFoundError(file_path)

        extension = path.suffix lowercased

        IF extension NOT IN self.readers:
            RAISE UnsupportedFileTypeError(extension)

        reader      = self.readers[extension]
        source_type = EXTENSION_TABLE[extension][1]

        LOG info: "reading <file_path> with <reader class name>"

        # [FILE READ] the real call — this line is Phase 0 item 2
        raw_record = reader.read(str(path))
        # raw_record is now a plain dict. BaseReader.get_base_metadata() gives:
        #   {file_path, file_name, file_size_bytes, file_extension, mime_type,
        #    file_hash_sha256, created_timestamp, modified_timestamp,
        #    processed_timestamp, reader_class}
        # plus reader-specific text fields on top.

        RETURN self._to_internal_document(raw_record, source_type)


    FUNCTION _handle_raw_text(self, text) -> InternalDocument:

        # Text handed in directly — no file, so no reader and no file metadata.
        # Build the minimal raw_record the converter expects, then take the SAME
        # path as a file. One construction site, one set of rules.
        IF text is empty or only whitespace:
            RAISE NoTextFoundError("raw_text was empty")

        raw_record = {
            "raw_content":  text,
            "reader_class": "raw_text",
        }
        RETURN self._to_internal_document(raw_record, SourceType.FILE_TXT)


    # ══ THE ONE CONVERSION SITE ═══════════════════════════════
    # Hard rule: readers return dicts, ONLY this function builds an
    # InternalDocument. If a second place ever constructs one, the contract
    # is broken and nothing downstream can trust the shape.

    FUNCTION _to_internal_document(self, raw_record, source_type) -> InternalDocument:

        text = self._extract_text(raw_record)

        # Prefer the file's content hash if the reader computed one, else hash
        # the text. Both are deterministic: same bytes, same ID, forever, with
        # no database and no counter.
        document_id = raw_record.get("file_hash_sha256")
                      OR _hash_to_document_id(text)

        RETURN InternalDocument(
            document_id         = document_id,
            text                = text,
            source_type         = source_type,
            ingestion_timestamp = raw_record.get("processed_timestamp")
                                  OR current time as ISO string,      # see D1
            source_metadata     = raw_record,     # everything the reader found
            language            = raw_record.get("language"),
            title               = raw_record.get("title") OR raw_record.get("file_name"),
            author              = raw_record.get("author"),
            tables              = raw_record.get("tables",   default empty list),
            images              = raw_record.get("images",   default empty list),
            sections            = raw_record.get("sections", default empty list),
            quality_flags       = raw_record.get("quality_indicators", default empty dict),
            processing_status   = ProcessingStatus.INGESTED,
        )


    FUNCTION _extract_text(self, raw_record) -> str:

        # Readers disagree on what they call the text field: PDFs give
        # full_raw_text, HTML gives extracted_text, TXT gives raw_content.
        # Try each in priority order rather than forcing every reader to conform.
        FOR EACH field IN ["full_raw_text", "extracted_text", "raw_content",
                           "text", "content", "body"]:
            value = raw_record.get(field)
            IF value is a non-empty string after stripping:
                RETURN value stripped

        # Structured readers (DOCX) give paragraphs instead of one blob.
        IF raw_record has "paragraphs" AND it is a non-empty list:
            RETURN the paragraphs joined with blank lines between them

        # Nothing usable. RAISE — do not stringify the record as a fallback (D2).
        RAISE NoTextFoundError("no text field in record from "
                               + raw_record.get("reader_class"))


    # ══ BATCH ═════════════════════════════════════════════════

    FUNCTION process_directory(self, directory, recursive = True,
                               output_file = "internal_documents.jsonl") -> dict:

        directory = Path(directory)
        IF directory does not exist:
            RAISE FileNotFoundError(directory)

        IF recursive: files = every file under directory at any depth
        ELSE:         files = every file directly inside directory

        # Sorted, so two runs over the same folder produce the same JSONL in the
        # same order. Filesystem listing order is not guaranteed, and this sort
        # is what makes the rerun byte-identical.
        SORT files by their path string

        stats = {total: count(files), success: 0, failed: 0, skipped: 0}

        OPEN (self.output_dir / output_file) for writing as out:
            FOR EACH file IN files:
                TRY:
                    doc = self.route_push_input(file_path = str(file))
                    # [FILE WRITE] one JSON object per line
                    WRITE doc.to_jsonl() + newline TO out
                    stats.success += 1

                CATCH UnsupportedFileTypeError:
                    # Expected and boring — a folder contains README.png.
                    # Counted as skipped, not failed: it must not look like a bug.
                    stats.skipped += 1

                CATCH any other Exception AS e:
                    stats.failed += 1
                    LOG error with the filename
                    self._log_error({"file_path": str(file)}, e)
                    CONTINUE          # one bad file must not kill the batch

        LOG info: "<success>/<total> succeeded, <skipped> skipped, <failed> failed"
        RETURN stats


    FUNCTION _log_error(self, raw_record, error):
        # Append-only failure log. A separate file means a bad batch leaves a
        # readable trail instead of scrolling past in the console.
        entry = {timestamp:  now as ISO string,
                 error:      text of error,
                 error_type: class name of error,
                 record:     raw_record}
        # [FILE WRITE] append mode
        APPEND json of entry + newline TO (self.output_dir / "errors.jsonl")
```

---

## 5. Build order

Each step is testable on its own before moving to the next.

1. **Fix the import line.** Drop `UnsupportedInputError`, drop the `ingest_clients` import.
   Confirm `import io_adapters.input_router` succeeds. Nothing else can be tested until this passes.
2. `EXTENSION_TABLE` + `__init__` + `_handle_file_path` + `_to_internal_document` +
   `_extract_text`. Run it on one real `.txt`. Print `doc.document_id` and `doc.text[:80]`.
3. Run the same file twice. Same `document_id` both times — your first determinism check.
4. Try a `.pdf` and a `.png`. PDF works; PNG gives `UnsupportedFileTypeError`, **not**
   `AttributeError`. If you get `AttributeError`, the extension table has a row it should not.
5. `_handle_raw_text` + `route_push_input`.
6. `process_directory` + `_log_error`. Point it at a folder holding one good file, one
   unsupported file, and one corrupt file — assert `stats` is `{success:1, skipped:1, failed:1}`.

## 6. Tests this module owes

Not yet written; belongs in `tests/test_input_router.py`.

- same file read twice produces the same `document_id`
- `document_id` equals the reader's `file_hash_sha256` when the reader supplies one
- `.png` raises `UnsupportedFileTypeError`
- a `.txt` containing only whitespace raises `NoTextFoundError`
- `route_push_input()` with no arguments raises `InvalidInputError`
- `process_directory` over a mixed folder returns the expected `stats` counts and does not abort
