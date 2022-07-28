CREATE SCHEMA IF NOT EXISTS bbc_case_study_staging
  OPTIONS (
    description = 'Staging dataset for external tables on files in the cloud storage');

CREATE SCHEMA IF NOT EXISTS bbc_case_study
  OPTIONS (
    description = 'Main dataset to store bigquery objects related to the case study');