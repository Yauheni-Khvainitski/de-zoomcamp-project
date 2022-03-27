# DOCUMENTATION for the project #

## Problem description ##
The aim of the project is to deliver metrics calculations based on a finanncial trading market data. **Deutsche Börse Public Dataset** used.

Metrics are:
* [implied volatility](https://www.investopedia.com/terms/i/iv.asp#:~:text=Volatility%20(IV)%20Works-,Implied%20volatility%20is%20the%20market's%20forecast%20of%20a%20likely%20movement,the%20symbol%20%CF%83%20(sigma).) of the traded securities/instruments 
* most traded securities/instruments by traded volume

Source data links: https://registry.opendata.aws/deutsche-boerse-pds/
Overall description: https://github.com/Deutsche-Boerse/dbg-pds
Data dictionary: https://github.com/Deutsche-Boerse/dbg-pds/blob/master/docs/data_dictionary.md.


## Cloud technologies used ##

The source data is **AWS S3**.

But for the pipeline mainly will be used:
* **GCP** (VM with Apache Airflow, data lake in Google Cloud Storage, Google Data Studio for visualisations)
* **dbt cloud** for building reporting tables.


## Data ingestion (batch) ##

Data ingestion pipeline uses Airflow DAG 



## Improvements to do: ##
- separate service accounts for diff services with own permissions (airflow, dbt)
- group multiple files to .parquet and then send to GCS
- partition BigQuery external table by Date
- tests and documentation for dbt project
- fix git pull for terraform "metadata_startup_script", consider changing to .sh script
