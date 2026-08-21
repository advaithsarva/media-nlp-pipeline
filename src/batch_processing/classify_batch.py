"""Run the pipeline over a folder of documents, in one process.

This is the batch entry point that always works. Ray and Spark do the same job across
more machines; this one needs nothing but the pipeline itself, so it is what Airflow calls
by default and what the distributed versions are checked against.

    python -m batch_processing.classify_batch --input data/raw --pattern "*.txt"

Determinism holds across a batch as well as within one document: files are processed in
sorted order and each document is scored independently of the others, so the same folder
always produces the same output file.
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from io_adapters.storage_clients import StorageClientFactory     # noqa: E402
from main import PipelineRunner                                  # noqa: E402


def classify_batch(input_dir=None, pattern="*.txt", conf_dir=None, output_config=None):
    """Process every matching file and return (records, failures).

    Failures are collected rather than raised. One unreadable file in a folder of a
    thousand should not lose the other nine hundred and ninety-nine -- but it must not
    disappear silently either, so it comes back in the second list.
    """
    runner = PipelineRunner(conf_dir) if conf_dir else PipelineRunner()

    input_dir = Path(input_dir) if input_dir else Path(
        runner.pipeline_conf.get("input", {})
        .get("sources", {}).get("files", {}).get("path", "data/raw")
    )

    records = []
    failures = []
    # sorted: the order the filesystem lists files in is not stable between machines
    for path in sorted(input_dir.glob(pattern)):
        if not path.is_file():
            continue
        try:
            records.append(runner.process_document(str(path)))
        except Exception as error:
            failures.append({"file": str(path), "error": str(error),
                             "error_type": type(error).__name__})

    if records:
        config = output_config or runner.pipeline_conf.get("output", {})
        StorageClientFactory.create(config).save_batch(records)

    return records, failures


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run the pipeline over a folder.")
    parser.add_argument("--input", help="folder of documents (default: from config)")
    parser.add_argument("--pattern", default="*.txt")
    parser.add_argument("--conf", help="config directory")
    parser.add_argument("--report", help="write a run summary here as JSON")
    args = parser.parse_args(argv)

    records, failures = classify_batch(args.input, args.pattern, args.conf)

    summary = {
        "processed": len(records),
        "failed": len(failures),
        "failures": failures,
        # document ids, sorted, so two runs of the same folder produce the same summary
        "document_ids": sorted(r["document_id"] for r in records),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))

    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(
            json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # a non-zero exit tells Airflow the task failed
    return 1 if failures and not records else 0


if __name__ == "__main__":
    raise SystemExit(main())
