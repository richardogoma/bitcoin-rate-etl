import sys
import time
from datetime import datetime
from etl.extract.retriever import retrieve_rates
from etl.transform.parser import parse_dict
from etl.load.loader import load_data
import requests
import sqlite3


def start_etl(config):
    try:
        while True:
            response = retrieve_rates(uri=config.API_URI)
            # print(f"Response of {type(response)} \n{response}")

            parsed_data = parse_dict(response)
            # print(f"Response of {type(parsed_data)} \n{parsed_data}")

            if not load_data(config.DATABASE_URI, parsed_data):
                raise IOError("Error loading data to SQLite db")
            else:
                print(
                    f"{datetime.now()}: INFO: Inserted {parsed_data[1]} rates as at {parsed_data[0].isoformat()} into database ..."
                )

            # Wait for one minute before fetching the next update
            time.sleep(60)

    except (requests.exceptions.RequestException, sqlite3.Error) as error_msg:
        print("Error: " + str(error_msg))
        sys.exit()
