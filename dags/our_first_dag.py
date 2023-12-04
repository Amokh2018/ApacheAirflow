from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner' : 'Ali',
    'retries' : 5,
    'retry_delay' : timedelta(minutes=2)
    

}
# create a simple DAG to run on Airflow:
with DAG(
    dag_id='our_first_dag_v3',
    default_args=default_args,
    description='This is our first dag that we write',
    start_date=datetime(2023, 7, 29, 2),
    schedule_interval='@daily' # every day at 2:00 AM

) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command='echo hello world, this is the first task!'
    )
    task2 = BashOperator(
        task_id='second_task',
        bash_command='echo hello world, this is the second task!'
    )
    task3 = BashOperator(
        task_id='third_task',
        bash_command='echo hello world, this is the third task!'
    )

# Task dependencies
    task1.set_downstream(task2)
    task1.set_downstream(task3)

    # second method:
    # task1 >> task2
    # task1 >> task3
    