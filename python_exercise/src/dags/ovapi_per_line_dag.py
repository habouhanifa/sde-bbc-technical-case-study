import os

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor

from datetime import datetime, timedelta

from libraries.processing.job import Extractor
from libraries.utils.utils import ConfLoader

default_args = {
    'start_date': datetime(2022, 7, 24),
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

ENDPOINT = ConfLoader.load_conf('api')['endpoint']


def fn_upload_data_to_gcs():
    job = Extractor()
    job.run()


with DAG(dag_id='ovapi_per_line_dag',
         schedule_interval='@daily',
         default_args=default_args,
         catchup=False) as dag:
    check_if_api_available = HttpSensor(task_id='check_if_api_available',
                                        http_conn_id='OVAPI_NL',
                                        endpoint=ENDPOINT,
                                        response_check=lambda response: "DataOwnerCode" in response.text,
                                        poke_interval=5,
                                        timeout=20
                                        )

    upload_data_to_gcs = PythonOperator(task_id='upload_data_to_gcs',
                                        python_callable=fn_upload_data_to_gcs)

    check_if_api_available >> upload_data_to_gcs
