from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.http.sensors.http import HttpSensor

from libraries.processing.jobs import Extractor, Validator, Cleaner
from libraries.utils.utils import ConfLoader
from libraries.sql import SQL_FOLDER

default_args = {
    'start_date': datetime(2022, 7, 24),
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

ENDPOINT = ConfLoader.load_conf('api')['endpoint']
BUCKET_NAME = ConfLoader.load_conf('gcs')['bucket-name']


def fn_upload_data_to_gcs(ti):
    job = Extractor()
    staged_file = job.run()
    ti.xcom_push(key='staged_file', value=staged_file)


def fn_run_data_validation(ti):
    staged_file = ti.xcom_pull(key='staged_file', task_ids=['upload_data_to_gcs'])[0].strip()
    job = Validator(staged_file)
    is_successful = job.run()
    if is_successful:
        return "create_external_table"
    else:
        return "end"


def fn_clean_temporay_folders():
    job = Cleaner()
    job.run()


with DAG(dag_id='ovapi_per_line_dag',
         schedule_interval='@daily',
         default_args=default_args,
         catchup=False,
         template_searchpath=f'{SQL_FOLDER}/') as dag:
    start = EmptyOperator(task_id='start')
    check_if_api_available = HttpSensor(task_id='check_if_api_available',
                                        http_conn_id='OVAPI_NL',
                                        endpoint=ENDPOINT,
                                        response_check=lambda response: "DataOwnerCode" in response.text,
                                        poke_interval=5,
                                        timeout=20
                                        )

    upload_data_to_gcs = PythonOperator(task_id='upload_data_to_gcs',
                                        python_callable=fn_upload_data_to_gcs)

    run_data_validation = BranchPythonOperator(task_id='run_data_validation',
                                               python_callable=fn_run_data_validation,
                                               do_xcom_push=False)

    create_external_table = BigQueryExecuteQueryOperator(task_id='create_external_table',
                                                         sql='ddl/EXT_OVAPI_NL_LINES.sql',
                                                         use_legacy_sql=False)

    load_data_to_target_table = BigQueryExecuteQueryOperator(task_id='load_data_to_target_table',
                                                             sql='dml/OVAPI_NL_LINES.sql',
                                                             use_legacy_sql=False)

    clean_temporary_folders = PythonOperator(task_id='clean_temporary_folders',
                                            python_callable=fn_clean_temporay_folders)

    end = EmptyOperator(task_id='end')

    start >> check_if_api_available
    check_if_api_available >> upload_data_to_gcs >> run_data_validation
    run_data_validation >> create_external_table >> load_data_to_target_table
    run_data_validation >> clean_temporary_folders >> end
    load_data_to_target_table >> clean_temporary_folders >> end
