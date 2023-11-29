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
You might not need all the services included, so the modified YAML file is [here]()
