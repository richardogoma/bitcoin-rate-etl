install:
	pip install --upgrade pip && \
		pip install -r requirements.txt

test:
	python -m pytest -vv --cov=etl.extract.retriever --cov=etl.transform.parser --cov=etl.load.loader \
		tests/test_data_retrieval.py tests/test_data_parsing.py tests/test_data_loading.py

format:
	black *.py **/*.py ***/**/*.py 

lint:
	pylint *.py **/*.py ***/**/*.py 

all: install format lint test