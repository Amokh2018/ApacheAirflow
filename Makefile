install:
	pip install --user --upgrade pip &&\
		pip install --no-cache-dir --user -r /requirements.txt

test:
	python -m pytest -vv --cov=main --cov=mylib test_*.py

format:	
	black *.py hugging-face/zero_shot_classification.py hugging-face/hf_whisper.py

lint:
	

container-build:
	docker build . --tag extending_airflow:latest

airflow-update:
	docker-compose up -d --no-deps --build airflow-webserver airflow-scheduler

container-lint:
	docker run --rm -i hadolint/hadolint < Dockerfile


refactor: format lint

deploy:
	#deploy goes here
		
all: install lint test format deploy