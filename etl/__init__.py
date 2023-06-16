"""
ETL module for data extraction, transformation, and loading.
"""

import sys
import time
from datetime import datetime
import sqlite3
import requests
from etl.extract.retriever import retrieve_rates
from etl.transform.parser import parse_dict
from etl.load.loader import load_data


def start_etl(config):
    """
    Start the ETL process.

    This function continuously retrieves data, transforms it, and loads it into the database.

    Args:
        config (Config): Configuration object containing API URI and database URI.
    """
    try:
        sqlite_db_path = config.get_config_value("DATABASE_URI")
        api_url = config.get_config_value("API_URI")

        while True:
            response = retrieve_rates(uri=api_url)
            parsed_data = parse_dict(response)

            if load_data(database_uri=sqlite_db_path, data=parsed_data):
                info = f"{parsed_data[1]} rates as at {parsed_data[0].isoformat()}"
                print(f"{datetime.now()}: INFO: Inserted {info} into the database ...")
            else:
                info = f"{parsed_data[1]} rates as at {parsed_data[0].isoformat()}"
                print(f"{datetime.now()}: INFO: Updated {info} in the database ...")

            # Wait for one minute before fetching the next update
            time.sleep(60)

    except (requests.exceptions.RequestException, sqlite3.Error) as error_msg:
        print("Error: " + str(error_msg))
        sys.exit()
