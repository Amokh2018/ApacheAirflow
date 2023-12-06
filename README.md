# ApacheAirflow
Learn about Apache Airflow


## How to Install and Setup
* [Install Steps](https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html)
```bash
$ pip install "apache-airflow[celery]==2.7.3" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.7.3/constraints-3.8.txt"
```
* To have everything in the project directory:
```bash
$ export AIRFLOW_HOME=.
```
* Initialise Database:
```bash
$ airflow db init
```
* Start the web server:
```bash
$ airflow webserver -p 8080
```
* Create a new user:
```bash
$ airflow users  create --role Admin --username user --email admin --firstname admin --lastname admin --password password
```
* In order to execute the DAGs, we have to start the airflow scheduler:
```bash
$ export AIRFLOW_HOME=.
$ airflow scheduler
```



## Run Airflow in Docker
* [Install Steps](https://airflow.apache.org/docs/apache-airflow/2.2.4/start/docker.html)
* Fetch the `docker-compose.yaml`:
```bash
$ curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.2.4/docker-compose.yaml'
```
You might not need all the services included, so the modified YAML file is [here](https://github.com/Amokh2018/ApacheAirflow/blob/main/docker-compose.yaml)
* Setting the right user
```bash
$ mkdir -p ./dags ./logs ./plugins
$ echo -e "AIRFLOW_UID=$(id -u)" > .env #for linux users only
```

* Initialize the database:
```bash
$ docker-compose up airflow-init
```

* Running Airflow:
```bash
$ docker-compose up -d
```
and you can check running containers:

```bash
$ docker ps
```
* Cleaning up everythin:
```bash
$ docker-compose down --volumes --rmi all
```

## Create first DAG:
* In the dags folder, create a python file :`firstdag.py`:
```python
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
```
Then open the airflow UI in the browser : `localhost:8080/home`, username: airflow, password: airflow, and refresh the dags to see the first DAG

## Create a DAG with python operator:
* Create a new DAG python file similar to the first one, and a python function called `greet(name, age)`: 
```python
def greet(name. age):
    print(f'Hello world! my name is {name}, 'f'and I am {age} years old.')
```
 that will be called by the python operator:
 ```python
task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        op_kwargs={'name':'Ali', 'age': 20} # pass the arguments to the python function greet()
    )
```

* Share Data via xComs between functions:
First, python function should pull and push data through xcom to share their results:
 ```python
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
```  
And then the tasks are run in order to generate and share the data:
```python
with DAG(
    dag_id='our_dag_with_python_operator_v05',
    default_args=default_args,
    description='This is our first dag using python operator',
    schedule_interval='@daily' # every day at 2:00 AM
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        #op_kwargs={'age': 20} # pass the arguments to the python function greet()
    )
    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name)

    task3 = PythonOperator(
        task_id='get_age',
        python_callable=get_age)
    
    [task2, task3] >> task1 # set the task2 as a downstream task of task1
```
## TaskFlow API
You can write the same DAG with less code using decorators from taskflow api:
```python
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
```
    