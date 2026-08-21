"""Batch runs must give the same answer as running the documents one at a time.

The whole reason distribution is safe here is that documents are scored independently --
no stage looks at another document. These tests are what turn that from a claim into a
checked property.
"""

import ast
import json
import shutil

import pytest

from conftest import ROOT
from batch_processing.classify_batch import classify_batch
from main import PipelineRunner


@pytest.fixture(scope="module")
def corpus(tmp_path_factory):
    """A folder with five slightly different articles plus one unreadable file."""
    folder = tmp_path_factory.mktemp("corpus")
    source = (ROOT / "data" / "raw" / "sample_article.txt").read_text(encoding="utf-8")
    for i in range(5):
        (folder / ("article_%d.txt" % i)).write_text(
            source.replace("transport bill", "transport bill number %d" % i),
            encoding="utf-8",
        )
    return folder


def test_batch_processes_every_file(corpus, tmp_path):
    records, failures = classify_batch(
        corpus, "*.txt", output_config={"type": "jsonl", "path": str(tmp_path)})

    assert len(records) == 5
    assert failures == []


def test_batch_matches_one_at_a_time(corpus, tmp_path):
    """A batch run and five separate runs must produce identical records."""
    batch, _ = classify_batch(
        corpus, "*.txt", output_config={"type": "jsonl", "path": str(tmp_path)})

    runner = PipelineRunner()
    individually = [runner.process_document(str(p)) for p in sorted(corpus.glob("*.txt"))]

    assert json.dumps(batch, sort_keys=True) == json.dumps(individually, sort_keys=True)


def test_batch_is_repeatable(corpus, tmp_path):
    first, _ = classify_batch(corpus, "*.txt",
                              output_config={"type": "jsonl", "path": str(tmp_path / "a")})
    second, _ = classify_batch(corpus, "*.txt",
                               output_config={"type": "jsonl", "path": str(tmp_path / "b")})

    assert (tmp_path / "a" / "records.jsonl").read_bytes() == \
           (tmp_path / "b" / "records.jsonl").read_bytes()


def test_one_bad_file_does_not_lose_the_others(corpus, tmp_path):
    """A folder with an unsupported file must still process the rest, and say what failed."""
    workspace = tmp_path / "mixed"
    shutil.copytree(corpus, workspace)
    (workspace / "notes.md").write_text("", encoding="utf-8")   # empty: no text to extract

    records, failures = classify_batch(
        workspace, "*.*", output_config={"type": "jsonl", "path": str(tmp_path / "out")})

    assert len(records) == 5
    assert len(failures) == 1
    assert failures[0]["file"].endswith("notes.md")
    assert failures[0]["error_type"]


def test_ray_gives_the_same_records_as_a_single_process(corpus, tmp_path):
    """The point of the sort in ray_preprocess: distribution must not change the answer."""
    ray = pytest.importorskip("ray")
    from batch_processing.preprocess_ray import ray_preprocess

    distributed, failures = ray_preprocess(str(corpus), "*.txt", workers=3)
    single, _ = classify_batch(
        corpus, "*.txt", output_config={"type": "jsonl", "path": str(tmp_path)})
    single.sort(key=lambda r: r["document_id"])

    assert failures == []
    assert json.dumps(distributed, sort_keys=True) == json.dumps(single, sort_keys=True)


def test_ray_worker_count_does_not_change_the_result(corpus):
    ray = pytest.importorskip("ray")
    from batch_processing.preprocess_ray import ray_preprocess

    with_one, _ = ray_preprocess(str(corpus), "*.txt", workers=1)
    with_five, _ = ray_preprocess(str(corpus), "*.txt", workers=5)

    assert json.dumps(with_one, sort_keys=True) == json.dumps(with_five, sort_keys=True)


def test_the_round_robin_split_keeps_every_item():
    from batch_processing.preprocess_ray import _split

    items = list(range(10))
    for workers in (1, 3, 4, 20):
        buckets = _split(items, workers)
        assert sorted(x for b in buckets for x in b) == items
        assert all(buckets)          # no empty buckets handed to a worker


# ---- the two that cannot be executed here, checked as far as they can be ----

def test_the_airflow_dag_parses():
    """Airflow does not run on Windows, so the DAG cannot be loaded -- but it must parse,
    and it must not contain NLP logic."""
    source = (ROOT / "airflow_dags" / "media_nlp_batch_dag.py").read_text(encoding="utf-8")
    tree = ast.parse(source)

    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
        elif isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)

    # the hard rule: Airflow orchestrates, it does not analyse
    assert "nlp_pipeline" not in imported
    assert "io_adapters" not in imported


def test_the_spark_job_parses():
    """Spark needs a JVM, which is not installed here. Syntax is still checkable."""
    source = (ROOT / "src" / "batch_processing" / "preprocess_spark.py").read_text(encoding="utf-8")
    ast.parse(source)
