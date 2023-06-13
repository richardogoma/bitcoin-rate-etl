[![Python application](https://github.com/richardogoma/bitcoin-rate-etl/actions/workflows/python-app.yml/badge.svg)](https://github.com/richardogoma/bitcoin-rate-etl/actions/workflows/python-app.yml)

# Bitcoin Rates ETL Pipeline
The project can be classified as a real-time streaming ETL (Extract, Transform, Load) pipeline. It is **part of [a Flask project](https://github.com/richardogoma/bitcoin-rate-tracker) focused on the development of a web application or microservice for tracking and visualizing Bitcoin rates across major currencies.**

The pipeline involves the following steps:

1. **Extract:** The ETL program extracts data from the CoinDesk Bitcoin Price Index API. It retrieves near-real-time data of Bitcoin rates across major currencies (USD/GBP/EUR). The data is obtained in the form of JSON payload.

2. **Transform:** The JSON payload is transformed to convert it into a structured format that is suitable for storage and analysis. This step involves parsing the JSON data, extracting relevant information such as timestamp, currency rates, and the chart name, and applying data transformations or manipulations.

3. **Load:** The transformed and structured data is loaded into an embedded (SQLite) database. This involves inserting the data into appropriate table within the database, ensuring data integrity, and handling any necessary updates or modifications to the existing data.

The ETL program is designed to run as a background process and perform these steps every minute to ensure the database stays up to date with the near-real-time Bitcoin rate data. The "every minute" condition was factored into the project design because the data at the API endpoint refreshes every 60 seconds. 

Overall, this pipeline enables the continuous extraction, transformation, and loading of data from the API into the SQLite database, providing the necessary data foundation for the Flask web application or microservice to track and visualize Bitcoin rates across major currencies.

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
source setup_etl.sh
```

## Disclaimer
The data was produced from the CoinDesk Bitcoin Price Index (USD). Non-USD currency data converted using hourly conversion rate from [openexchangerates.org](openexchangerates.org).
