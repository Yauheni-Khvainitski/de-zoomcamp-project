# de-zoomcamp-project
Development code for Data Engineering Zoomcamp project

**Improvements to do:**
- separate service accounts for diff services with own permissions (airflow, dbt)
- flexible DAGs (set bucket using vars, partition Date folder)
- group multiple files to .parquet and then send to GCS
- partition BigQuery external table by Date
- tests and documentation for dbt project
- fix git pull for terraform "metadata_startup_script", consider changing to .sh script
