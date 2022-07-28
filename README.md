# Senior-DE-BBC-technical-case-study

## Python Exercise
### Pre-requisits:

This mini project uses Airflow 2.3 using the Celery executor, each airflow instance runs on a docker container.
The tools needed to execute the project.
- Docker
- Python>=3.7
- (Optional) [gcloud CLI](https://cloud.google.com/sdk/docs/install) for recreating the table in BigQuery if needed 

### Clone the repo 

First, clone the repository from GitHub:
```
git clone https://github.com/habouhanifa/sde-bbc-technical-case-study.git
```

### Setting-up the development environment
 
To setup the development environment execute the `ìnstall.sh` script

```
./install.sh
```

This will create a python 3.7 virtual environment with all the modules needed for the development of the project.

### (Optional) Creating Schema and table in BigQuery
> This step is not necessary for the demo as the objects are already created 

To create the schemas and the target table needed for the project, you can run the following script:

```
./run_ddl.sh
```

### Start the project

The project components are all dockerized, and in order to start the project, we will use the script `run.sh`

```
./run.sh
```

This will execute a `docker-compose up` to start the different Docker containers.

### Run Demo:

Once all the containers are up, trigger the dag `ovapi_per_line_dag` to run the data pipeline.
To check the output of the pipeline, the ressources have been made public:

In GCS: Go to https://console.cloud.google.com/storage/browser/ovapi_nl_data_public
The prefixes:
- 01_RAW: Raw data in json format
- 02_STAGING: Data formatted in CSV format
- 03_READY: Files that passed the data quality checks
- 04_REJECTED: Files that failed the data quality checks
Each run creates a daily snapshot of the data, the file in GCS have the file pattern `ovapi_raw_data_YYYYMMDD.(json|csv)`

In BigQuery: Go to https://console.cloud.google.com/bigquery?project=lyrical-epigram-357400

#### Important:
>> Pin the project on the explorer tab and select your project

You now have access to the data in bigquery tables:

- `bbc_case_study_staging.ext_ovapi_nl_lines`: external table pointing to the latest validated file in GCS bucket
- `bbc_case_study.ovapi_nl_lines`: target table with data from the OVAPI Netherlands Per Line endpoint

> To reset the table `bbc_case_study.ovapi_nl_lines`, execute the script `reset_tables.sh`
>```
>./reset_tables.sh
>```

### Pipeline explanation:

The pipeline `ovapi_per_line_dag` is composed of 5 main tasks.

- `check_if_api_available`: a HTTP sensor that checks the availbility of the endpoint from which we pull data
- `upload_data_to_gcs`: runs a python job that consists of calling the endpoint and retrievieng data.
Then stores it locally as a json file containing raw data and upload it to the GCS bucket under the 01_RAW prefix.
Then transform the file to csv and upload it to the GCS bucket under the 02_STAGING prefix.
- `run_data_validation`: runs a python job that takes the file in 02_STAGING and runs some data validations using great expectations.
The validation rules are listed in `python_exercise/src/libraries/conf/expectations/ovapi_nl_lines.json` as a list of expectations.
If the file passes those expectations it will be uploded to the GCS bucket under the 03_READY prefix, and will continue processing.
If the file fails those expectations it will be uploded to the GCS bucket under the 04_REJECTED prefix, and will stop processing and skip to the end of the pipeline.
- `create_external_table`: Creates an external table pointing to the latest file with prefix 03_READY in the GCS bucket
- `load_data_to_target_table`: Executes a SQL query to upsert data in the external table to the target table
 