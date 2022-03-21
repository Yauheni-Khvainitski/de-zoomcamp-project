from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from utils.s3_tools import S3Tools as S3
from datetime import datetime

dag_id = 'load_xetra_data'

default_args = {
    'owner': 'khv',
    'depends_on_past': False,
    'start_date': datetime(2021, 1, 1), # use Variable
    'schedule_interval': "@daily",      # use Variable
}

s3 = S3('deutsche-boerse-xetra-pds')

def test():
    exec_date1 = "{{ ds }}"
    exec_date2 = "{{ execution_date }}"
    exec_date3 = '{{ execution_date.strftime("%Y-%m-%d") }}'
    print(exec_date1)
    print(exec_date2)
    print(exec_date3)

# files_list = s3.get_list_of_files(exec_date)

with DAG(
        dag_id,
        default_args=default_args,
        max_active_runs=1,
        max_active_tasks=16,
        catchup=False
) as dag:

    # s3_download = PythonOperator(
    #         task_id="s3_download",
    #         python_callable=s3.download_files,
    #         op_args=[files_list, exec_date]
    #     )

    # s3_download

    test = PythonOperator(
            task_id="test",
            python_callable=test,
        )

    test
