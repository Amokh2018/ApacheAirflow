from airflow.decorators import dag, task
from datetime import datetime, timedelta

default_args = {
    'owner': 'Ali',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

@dag(dag_id='dag_with_taskflow_api_v02',default_args=default_args,
     start_date=datetime(2022,1,1),schedule_interval='@daily')
def hello_world_dag():
    @task(multiple_outputs=True)
    def get_name():
        return {'first_name':'Ali', 'last_name':'Mokh'}

    @task
    def get_age():
        return 30
    
    @task
    def greet(first_name,last_name, age):
        print(f'Hello World! My name is {first_name} {last_name} and I am {age} years old')

    name = get_name()
    age = get_age()
    greet(first_name=name['first_name'], last_name=name['last_name'], age=age)
    
greet_dag = hello_world_dag()    

    