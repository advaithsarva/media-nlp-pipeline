from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

with DAG(
    "media_nlp_batch",
    schedule_interval="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:

    preprocess = BashOperator(
        task_id="preprocess",
        bash_command="python -m src.batch_processing.preprocess_spark",
    )

    classify = BashOperator(
        task_id="classify",
        bash_command="python -m src.batch_processing.classify_batch",
    )

    preprocess >> classify
