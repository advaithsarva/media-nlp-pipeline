"""Spark batch processing -- for corpora too large to sit on one filesystem.

Use this only when Ray has genuinely run out of room. Spark costs a JVM, a cluster and a
lot of operational surface; below roughly a hundred thousand documents it is slower than
`classify_batch` because the startup dominates.

    spark-submit --master local[4] src/batch_processing/preprocess_spark.py \
        --input data/raw --output data/processed/gold

Design notes worth knowing before reading the code:

* **mapPartitions, not map.** A PipelineRunner is built once per partition rather than once
  per document. Per document it would rebuild every compiled regex thousands of times.
* **The runner is never sent over the wire.** It holds compiled patterns and an open schema
  and would not pickle cleanly. Each worker constructs its own from config.
* **The result is a JSON string per document, not a nested Row.** Spark would need an
  explicit StructType for the nested findings and composites, and that schema would have to
  be kept in step with output_schema.json by hand. One string column cannot drift.
* **Sorted by document_id before writing**, so a Spark run and a single-process run over the
  same corpus produce the same content.

Not exercised on this machine: Spark needs a JVM, which is not installed here. The Ray path
is tested and does the same work.
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))


def _process_partition(paths, conf_dir=None):
    """Runs on a worker, once per partition. Yields one JSON string per document."""
    from main import PipelineRunner

    runner = PipelineRunner(conf_dir) if conf_dir else PipelineRunner()
    for path in paths:
        try:
            record = runner.process_document(path)
            yield json.dumps({"document_id": record["document_id"],
                              "record": json.dumps(record, sort_keys=True),
                              "error": None}, sort_keys=True)
        except Exception as error:
            # a bad file becomes a row, not a dead job
            yield json.dumps({"document_id": None, "record": None,
                              "error": str(path) + ": " + str(error)}, sort_keys=True)


def spark_preprocess(input_dir="data/raw", pattern="*.txt", output_dir=None,
                     conf_dir=None, master=None):
    from pyspark.sql import SparkSession

    builder = SparkSession.builder.appName("media_nlp_batch")
    if master:
        builder = builder.master(master)
    spark = builder.getOrCreate()

    try:
        paths = [str(p) for p in sorted(Path(input_dir).glob(pattern)) if p.is_file()]
        if not paths:
            return []

        # one partition per worker core, but never more partitions than documents
        partitions = min(len(paths), spark.sparkContext.defaultParallelism)
        rdd = spark.sparkContext.parallelize(paths, partitions)

        processed = rdd.mapPartitions(lambda chunk: _process_partition(chunk, conf_dir))
        rows = [json.loads(line) for line in processed.collect()]

        # sorted so the distributed result matches the single-process one; None ids
        # (failures) sort last rather than crashing the comparison
        rows.sort(key=lambda r: (r["document_id"] is None, r["document_id"] or ""))

        if output_dir:
            target = Path(output_dir)
            target.mkdir(parents=True, exist_ok=True)
            with open(target / "records.jsonl", "w", encoding="utf-8") as f:
                for row in rows:
                    if row["record"]:
                        f.write(row["record"] + "\n")

        return rows
    finally:
        spark.stop()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run the pipeline on Spark.")
    parser.add_argument("--input", default="data/raw")
    parser.add_argument("--pattern", default="*.txt")
    parser.add_argument("--output", default="data/processed/gold")
    parser.add_argument("--conf")
    parser.add_argument("--master", help="e.g. local[4]; omit under spark-submit")
    args = parser.parse_args(argv)

    rows = spark_preprocess(args.input, args.pattern, args.output, args.conf, args.master)
    errors = [r["error"] for r in rows if r["error"]]
    print(json.dumps({"processed": len(rows) - len(errors),
                      "failed": len(errors), "failures": errors},
                     indent=2, sort_keys=True))
    return 1 if errors and len(errors) == len(rows) else 0


if __name__ == "__main__":
    raise SystemExit(main())
