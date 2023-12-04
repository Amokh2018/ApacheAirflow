from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'Ali',
    'depends_on_past': False,
    'start_date': datetime(2023, 11, 29),
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def greet(ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name') # get the name from the previous task get_name()
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name') # get the name from the previous task get_name()
    age = ti.xcom_pull(task_ids='get_age', key='age') # get the age from the previous task get_age()
    print(f'Hello world! my name is {first_name} {last_name}, 'f'and I am {age} years old.')



def get_name(ti):
    ti.xcom_push(key='first_name', value='Ali') # push the name to the next task greet()
    ti.xcom_push(key='last_name', value='Mokh') # push the name to the next task greet()
    
def get_age(ti):
    ti.xcom_push(key='age', value=19) # push the age to the next task greet()
  
    
with DAG(
    dag_id='our_dag_with_python_operator_v05',
    default_args=default_args,
    description='This is our first dag using python operator',
    schedule_interval='@daily' # every day at 2:00 AM
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        #op_kwargs={'age': 20} # pass the arguments to the python function greet(
    )
    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name)

    task3 = PythonOperator(
        task_id='get_age',
        python_callable=get_age)
    
    [task2, task3] >> task1 # set the task2 as a downstream task of task1
