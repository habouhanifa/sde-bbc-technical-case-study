
CREATE OR REPLACE EXTERNAL TABLE bbc_case_study_staging.ext_ovapi_nl_lines
OPTIONS(
  format = 'CSV',
  field_delimiter = ';',
    skip_leading_rows =1,
  uris = ["gs://ovapi_nl_data_public/03_READY/{{ task_instance.xcom_pull(key='staged_file', task_ids=['upload_data_to_gcs'])[0].strip() }}"]
);
