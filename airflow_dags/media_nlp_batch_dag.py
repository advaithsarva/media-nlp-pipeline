"""Daily batch run.

Airflow orchestrates and contains no NLP logic -- that is a hard rule for this project. If
you find yourself importing anything from nlp_pipeline into this file, the logic belongs in
a batch script that Airflow calls instead.

    ingest_check -> analyse -> validate_output -> archive

Each task is a separate process, so a failure is isolated and Airflow can retry it. The
tasks talk to each other through files on disk, not through XCom: the run summary can be
several hundred kilobytes, and XCom is meant for small values.

Not run on this machine -- Airflow does not support Windows natively. The DAG is written to
be correct and to parse; the work it schedules is `batch_processing.classify_batch`, which
is tested.
"""

from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
REPORT = OUTPUT_DIR / "run_summary.json"

default_args = {
    "owner": "nlp",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    # do not start a run while the previous one is still going: two runs writing the same
    # output file would interleave their lines
    "depends_on_past": False,
}


def check_input_present(**context):
    """Fail early and clearly if there is nothing to process.

    Without this the analyse task succeeds having done nothing, and an empty output looks
    exactly like a clean corpus.
    """
    files = sorted(INPUT_DIR.glob("*.txt"))
    if not files:
        raise FileNotFoundError("no input documents in " + str(INPUT_DIR))
    return len(files)


def validate_output(**context):
    """Re-read the run summary and refuse to archive a run that mostly failed."""
    import json

    if not REPORT.exists():
        raise FileNotFoundError("no run summary at " + str(REPORT))

    summary = json.loads(REPORT.read_text(encoding="utf-8"))
    processed, failed = summary["processed"], summary["failed"]

    if processed == 0:
        raise ValueError("every document failed: " + json.dumps(summary["failures"][:5]))
    # a few bad files in a large corpus is normal; a majority failing is a broken run
    if failed > processed:
        raise ValueError("more failures (" + str(failed) + ") than successes ("
                         + str(processed) + ")")
    return summary


with DAG(
    dag_id="media_nlp_batch",
    description="Daily deterministic analysis of the incoming article corpus.",
    default_args=default_args,
    schedule="@daily",
    start_date=datetime(2026, 2, 21),
    catchup=False,
    max_active_runs=1,
    tags=["nlp", "media", "deterministic"],
) as dag:

    ingest_check = PythonOperator(
        task_id="ingest_check",
        python_callable=check_input_present,
    )

    # PYTHONPATH rather than an installed package, so the DAG works against a checkout
    analyse = BashOperator(
        task_id="analyse",
        bash_command=(
            "cd " + str(PROJECT_ROOT) + " && "
            "PYTHONPATH=src python -m batch_processing.classify_batch "
            "--input " + str(INPUT_DIR) + " --pattern '*.txt' "
            "--report " + str(REPORT)
        ),
    )

    validate = PythonOperator(
        task_id="validate_output",
        python_callable=validate_output,
    )

    # dated copy, so a bad config change can be spotted by diffing two days
    archive = BashOperator(
        task_id="archive",
        bash_command=(
            "cp " + str(OUTPUT_DIR / "records.jsonl") + " "
            + str(OUTPUT_DIR) + "/records-{{ ds }}.jsonl"
        ),
    )

    ingest_check >> analyse >> validate >> archive
