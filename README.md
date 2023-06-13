# Bitcoin Rates ETL Streaming Pipeline
The requirement for this project was to extract near-real time data of Bitcoin rates across major currencies `(USD/GBP/EUR)` from the CoinDesk Bitcoin Price Index API, do some transformations on the JSON payload and load structured data to an embedded (SQLite) database. 

The data at the API endpoint refreshes every 60 seconds, so this ETL program would run as a background process, extracting JSON data, transforming and loading structured data into the embedded database every minute.

This project is **part of a Flask project focused on the development of a web application or microservice for tracking and visualizing Bitcoin rates across major currencies.**

## The ETL project structure
```bash
 tree --dirsfirst --prune -I '*.pyc|__pycache__'
```
```
.
├── data
│   ├── processed
│   │   └── bitcoin_rate_tracker.db
│   └── raw
│       └── sample.json
├── etl
│   ├── extract
│   │   ├── __init__.py
│   │   └── retriever.py
│   ├── load
│   │   ├── __init__.py
│   │   └── loader.py
│   ├── transform
│   │   ├── __init__.py
│   │   └── parser.py
│   └── __init__.py
├── tests
│   ├── __init__.py
│   ├── test_data_loading.py
│   ├── test_data_parsing.py
│   └── test_data_retrieval.py
├── LICENSE
├── Makefile
├── README.md
├── config.py
├── etl_pipeline.py
├── output.log
├── requirements.txt
└── setup_etl.sh

8 directories, 21 files
```

## Setup ETL Pipeline
```bash
chmod +x setup_etl.sh && ./setup_etl.sh
```

## Disclaimer
The data was produced from the CoinDesk Bitcoin Price Index (USD). Non-USD currency data converted using hourly conversion rate from [openexchangerates.org](openexchangerates.org).