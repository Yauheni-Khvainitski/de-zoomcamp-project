# DOCUMENTATION for the project #


## Problem description ##
The aim of the project is to deliver metrics calculations based on a finanncial trading market data. **Deutsche Börse Public Dataset** used.

Metrics are:
* [implied volatility](https://www.investopedia.com/terms/i/iv.asp#:~:text=Volatility%20(IV)%20Works-,Implied%20volatility%20is%20the%20market's%20forecast%20of%20a%20likely%20movement,the%20symbol%20%CF%83%20(sigma).) of the traded securities/instruments 
* most traded securities/instruments by traded volume

Source data links: https://registry.opendata.aws/deutsche-boerse-pds/

Overall dataset description: https://github.com/Deutsche-Boerse/dbg-pds

Data dictionary: https://github.com/Deutsche-Boerse/dbg-pds/blob/master/docs/data_dictionary.md.


## Cloud technologies used ##

![project-architecture](https://user-images.githubusercontent.com/29374700/160330842-44360fa6-b42a-42be-a695-e366529227ac.jpg)

The source data is **AWS S3**.

But for the pipeline mainly will be used:
* **GCP** (VM with Apache Airflow, data lake in Google Cloud Storage, BigQuery for DWH, Google Data Studio for visualisations)
* **dbt cloud** for building reporting tables.

All the infrastructure deployed using Terraform. VM with Apache Airflow deployed using a Machine Image prepared in advance (with docker, docker-compose, and repo directory). The source code for deployment is [here](https://github.com/Yauheni-Khvainitski/de-zoomcamp-project/tree/main/terraform).


## Data ingestion (batch) ##

Data ingestion pipeline uses Airflow DAG load_xetra_data.

DAG has 3 tasks:

<img width="437" alt="image" src="https://user-images.githubusercontent.com/29374700/160300346-441933ef-0f09-4102-9461-7e3a908be38b.png">

* **s3_download** downloads data from S3 to the local worker storage (it uses [S3Tools](https://github.com/Yauheni-Khvainitski/de-zoomcamp-project/blob/main/airflow/dags/utils/s3_tools.py) class for reusable methods)

* **upload_to_raw_gcs** loads from local airflow worker storage to GCS data lake in deutsche_boerse bucket. [GCPTools](https://github.com/Yauheni-Khvainitski/de-zoomcamp-project/blob/main/airflow/dags/utils/gcp_tools.py) class is used for that.
Inside the bucket objects placed according to daily partitioning strategy for external tables:
<img width="302" alt="image" src="https://user-images.githubusercontent.com/29374700/160300601-ba0b8f1e-665b-4326-9eca-dbf9ff472d85.png">

* **remove_files** task cleans the airflow worker local storage using [FilesTools](https://github.com/Yauheni-Khvainitski/de-zoomcamp-project/blob/main/airflow/dags/utils/files_tools.py) class.

#### Batching strategy ####
DAG runs daily and takes data for the ended day (yesterday using daily schedule and {{ ds }} macro in airflow). So, for example DAG sarted 2022-03-27 will load data for 2022-03-26 to the data lake. Initially data loaded for 2022 year using catchup parameter. Code for the DAG is [here](https://github.com/Yauheni-Khvainitski/de-zoomcamp-project/blob/main/airflow/dags/load_xetra_data.py), variables are [here](https://github.com/Yauheni-Khvainitski/de-zoomcamp-project/blob/main/airflow/variables.json)


## Data warehouse ##

BigQuery used for DWH. Initial external table created using [separate script in repo](https://github.com/Yauheni-Khvainitski/de-zoomcamp-project/blob/main/bigquery_dwh/DS_DEUTSCHE_BOERSE/EXTERNAL_TABLES/ext_xetra_raw.sql).

Other objects created in BigQuery using dbt cloud. 


## Transformations ##

Data transformations are made with dbt cloud. Source code for models is [here](https://github.com/Yauheni-Khvainitski/de-zoomcamp-project/tree/main/dbt/models).

The data is rather clean, so, increment for last 40 days is put to **raw layer** from external table. And **mart layer** is built on top of it with metrics calculations. Google Data Studio will be connected to mart layer tables.

dbt job runs daily and refreshes data for last 7 and 30 days for specified metrics tables.

Job runs succesfully

<img width="1723" alt="image" src="https://user-images.githubusercontent.com/29374700/160331158-b58d6ed4-4720-43cd-b6d7-d3d942517ae6.png">

<img width="1154" alt="image" src="https://user-images.githubusercontent.com/29374700/160331213-66f689d7-b954-48f9-95a1-839d81f6d4b1.png">

All objects created in the target production dataset

<img width="361" alt="image" src="https://user-images.githubusercontent.com/29374700/160301901-9771713e-55ff-42c8-bb7c-e9c16f45c1b2.png">

## Dashboard ##




## Improvements to do: ##
- separate service accounts for diff services with own permissions (airflow, dbt)
- group multiple files to .parquet and then send to GCS
- partition BigQuery external table by Date
- tests and documentation for dbt project
- fix git pull for terraform "metadata_startup_script", consider changing to .sh script
