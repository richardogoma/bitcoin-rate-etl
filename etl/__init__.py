"""
ETL module for data extraction, transformation, and loading.
"""

import sys
import time
from datetime import datetime, timedelta
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
            start_time = time.time()
            response = retrieve_rates(uri=api_url)
            parsed_data = parse_dict(response)

            if load_data(database_uri=sqlite_db_path, data=parsed_data):
                end_time = time.time()
                process_duration = end_time - start_time
                info = f"{parsed_data[1]} rates as at {parsed_data[0].isoformat()}"
                print(
                    f"{datetime.now()}: INFO: Inserted {info} into the database. ETL process duration: {process_duration} secs"
                )
            else:
                end_time = time.time()
                process_duration = end_time - start_time
                info = f"{parsed_data[1]} rates as at {parsed_data[0].isoformat()}"
                print(
                    f"{datetime.now()}: INFO: Updated {info} in the database. ETL process duration: {process_duration} secs"
                )

            # Calculate the time until the next minute
            now = datetime.now()
            next_minute = now.replace(second=0, microsecond=0) + timedelta(minutes=1)

            # Wait until the next minute
            remaining_time = (next_minute - now).total_seconds()
            time.sleep(remaining_time)

    except (requests.exceptions.RequestException, sqlite3.Error) as error_msg:
        print("Error: " + str(error_msg))
        sys.exit()
