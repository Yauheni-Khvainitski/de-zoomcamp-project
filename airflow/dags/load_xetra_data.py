from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from utils.s3_tools import S3Tools as S3
import os
from utils.gcp_tools import GCPTools as GT
from utils.files_tools import FilesTools as FT

dag_id = 'load_xetra_data'

var = Variable.get(dag_id, deserialize_json=True)

# start_dt = datetime.today() - timedelta(var['define_start_date'])
# start_dt = datetime(start_dt.year, start_dt.month, start_dt.day)
start_dt = datetime(2022, 1, 1)
dag_schedule = var['dag_schedule']

default_args = {
    'owner': 'khv',
    'depends_on_past': False,
    'start_date': start_dt,
    'schedule_interval': dag_schedule
}

def get_load_dt(variables):
    if variables['load_dt'] == 'NULL':
        load_dt = '{{ ds }}'
    else:
        load_dt = variables['load_dt']
    return load_dt

load_dt = get_load_dt(var)
download_dir = var['download_dir']
gcs_raw_path = var['gcs_raw_path']

s3 = S3(var['S3_bucket'])
gt = GT(gcs_raw_path)
ft = FT()

with DAG(
        dag_id,
        default_args=default_args,
        max_active_runs=1,
        max_active_tasks=16,
        catchup=True,
        tags=var['dag_tags']
) as dag:

    s3_download = PythonOperator(
            task_id='s3_download',
            python_callable=s3.download_s3_files,
            op_args=[download_dir, load_dt]
        )

    upload_to_raw_gcs = PythonOperator(
            task_id='upload_to_raw_gcs',
            python_callable=gt.upload_to_gcs,
            op_args=[download_dir, load_dt]
        )

    remove_files = PythonOperator(
            task_id='remove_files',
            python_callable=ft.remove_from_dir,
            op_args=[os.path.join(download_dir, load_dt)]
        )

    s3_download >> upload_to_raw_gcs >> remove_files
