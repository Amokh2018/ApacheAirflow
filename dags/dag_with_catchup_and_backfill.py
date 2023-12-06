from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'Ali',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}
with DAG(
    dag_id='dag_with_catchup_backfill_v02',
    default_args=default_args,
    start_date=datetime(2023, 11, 10),
    schedule_interval='@daily', # every day at 2:00 AM
    catchup=True
) as dag:
    
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo this is simple bash command'
    )

