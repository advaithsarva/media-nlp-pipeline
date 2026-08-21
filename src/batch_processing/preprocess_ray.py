"""Distributed batch processing with Ray -- the same work as classify_batch, spread across
CPU cores or a small cluster.

Ray is the right middle rung: heavier than a for-loop, far lighter than Spark, and it runs
on one laptop as happily as on twenty machines. Reach for Spark only when the corpus stops
fitting on a single filesystem.

    python -m batch_processing.preprocess_ray --input data/raw --workers 4

The thing that makes this safe to distribute: documents are scored independently. No stage
looks at another document, so splitting the list across workers cannot change any result.
Order is restored by sorting on document_id at the end, which is why the distributed output
matches the single-process output byte for byte -- there is a test for exactly that.

Each worker builds its own PipelineRunner. That sounds wasteful and is not: a runner holds
compiled regexes and a loaded JSON schema, neither of which can be shared across processes,
and building one takes a few milliseconds against seconds of work per batch.
"""

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))


def _process_chunk(paths, conf_dir=None):
    """Runs inside a worker. Takes file paths, returns finished records.

    Paths cross the process boundary, not documents: sending a path is a few bytes,
    sending parsed text and tokens would be megabytes.
    """
    from main import PipelineRunner

    runner = PipelineRunner(conf_dir) if conf_dir else PipelineRunner()
    records, failures = [], []
    for path in paths:
        try:
            records.append(runner.process_document(path))
        except Exception as error:
            failures.append({"file": path, "error": str(error),
                             "error_type": type(error).__name__})
    return records, failures


def _split(items, parts):
    """Deal the items out round-robin so every worker gets a similar amount."""
    buckets = [[] for _ in range(max(parts, 1))]
    for i, item in enumerate(items):
        buckets[i % len(buckets)].append(item)
    return [b for b in buckets if b]


def ray_preprocess(input_dir="data/raw", pattern="*.txt", workers=4, conf_dir=None):
    import ray

    paths = [str(p) for p in sorted(Path(input_dir).glob(pattern)) if p.is_file()]
    if not paths:
        return [], []

    # Ray workers are fresh processes and do not inherit this one's sys.path, so without
    # PYTHONPATH they cannot import batch_processing and fail while unpickling the task.
    # os.pathsep because the separator is ";" on Windows and ":" everywhere else.
    src = str(ROOT / "src")
    existing = os.environ.get("PYTHONPATH", "")
    worker_path = src if not existing else src + os.pathsep + existing

    # ignore_reinit_error so calling this twice in one process (a test, a notebook)
    # does not blow up on an already-running Ray instance
    ray.init(
        ignore_reinit_error=True,
        log_to_driver=False,
        runtime_env={"env_vars": {"PYTHONPATH": worker_path}},
    )
    try:
        remote_chunk = ray.remote(_process_chunk)
        jobs = [remote_chunk.remote(chunk, conf_dir) for chunk in _split(paths, workers)]
        results = ray.get(jobs)
    finally:
        ray.shutdown()

    records, failures = [], []
    for chunk_records, chunk_failures in results:
        records.extend(chunk_records)
        failures.extend(chunk_failures)

    # Workers finish in whatever order they finish. Sorting here is what makes a
    # distributed run produce the same bytes as a single-process one.
    records.sort(key=lambda r: r["document_id"])
    failures.sort(key=lambda f: f["file"])
    return records, failures


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run the pipeline across Ray workers.")
    parser.add_argument("--input", default="data/raw")
    parser.add_argument("--pattern", default="*.txt")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--conf")
    parser.add_argument("--save", action="store_true",
                        help="store the records using the configured writer")
    args = parser.parse_args(argv)

    records, failures = ray_preprocess(args.input, args.pattern, args.workers, args.conf)

    if args.save and records:
        from io_adapters.storage_clients import StorageClientFactory
        from main import load_configs
        pipeline_conf = load_configs(args.conf)[0] if args.conf else load_configs()[0]
        StorageClientFactory.create(pipeline_conf.get("output", {})).save_batch(records)

    print(json.dumps({"processed": len(records), "failed": len(failures),
                      "failures": failures}, indent=2, sort_keys=True))
    return 1 if failures and not records else 0


if __name__ == "__main__":
    raise SystemExit(main())
