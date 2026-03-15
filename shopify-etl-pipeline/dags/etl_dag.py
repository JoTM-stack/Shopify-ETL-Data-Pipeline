from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys

sys.path.append("c:\Users\YourPC\Downloads\shopify-etl-pipeline\shopify_etl")


# If you are using WSL
# sys.path.append("/mnt/c/Users/YourPC/Downloads/shopify-etl-pipeline/shopify_etl")

from main import run

default_args = {
    "owner": "airflow",
    "start_date": datetime(2026, 3, 1),
}

with DAG(
    dag_id="shopify_etl_pipeline",
    default_args=default_args,
    schedule=None,
    catchup=False,
) as dag:

    run_pipeline = PythonOperator(
        task_id="run_shopify_pipeline",
        python_callable=run,
    )