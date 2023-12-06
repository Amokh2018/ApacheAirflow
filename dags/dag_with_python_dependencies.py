from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'Ali',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def get_sklearn():
    import sklearn  
    print(f"sklearn version is: {sklearn.__version__}")

def get_matplotlib():
    import matplotlib
    print(f"matplotlib version is: {matplotlib.__version__}")
with DAG(
    dag_id='dag_with_scikit_learn_v03',
    default_args=default_args,
    start_date=datetime(2023, 11, 10),
    schedule_interval='@daily'
) as dag:
    
    get_sklearn = PythonOperator(
        task_id='get_sklearn',  
        python_callable=get_sklearn
    )

    get_matplotlib = PythonOperator(
        task_id='get_matplotlib',
        python_callable=get_matplotlib
    )
    
    get_matplotlib >> get_sklearn 