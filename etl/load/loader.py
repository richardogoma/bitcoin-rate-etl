import sqlite3
import sys
from decimal import Decimal
from datetime import datetime


def load_data(database_uri: str, data: list) -> bool:
    schema = {
        "database_name": "bitcoin_rate_tracker",
        "schema_name": "dbo",
        "table": "bitcoin_rates",
        "fields": {
            "unique_number": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "timestamp": "DATETIME2 NOT NULL",
            "chart_name": "VARCHAR(10) NOT NULL",
            "usd_rate": "DECIMAL(18, 4) NOT NULL",
            "gbp_rate": "DECIMAL(18, 4) NOT NULL",
            "eur_rate": "DECIMAL(18, 4) NOT NULL",
        },
    }

    try:
        # Prepare the data for insertion
        formatted_data = [
            str(item)
            if isinstance(item, Decimal)
            else item.isoformat()
            if isinstance(item, datetime)
            else str(item)
            for item in data
        ]

        # Connect to SQLite database
        connection = sqlite3.connect(database_uri)
        with connection:
            cursor = connection.cursor()

            # Create table schema
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {schema['table']} (
                {', '.join(f'{column} {specification}' for column, specification in schema['fields'].items())},
                UNIQUE (timestamp)
            );
            """
            cursor.execute(create_table_query)

            # Insert data into SQLite table
            insert_query = f"""
            INSERT INTO {schema['table']} ({', '.join(field for field in schema['fields'] if field != 'unique_number')})
            VALUES ({', '.join(['?'] * (len(schema['fields']) - 1))})
            ON CONFLICT (timestamp) DO UPDATE SET
                {', '.join(f"{field} = excluded.{field}" for field in schema['fields'] if field != 'unique_number' and field != 'timestamp')}
            """
            cursor.execute(insert_query, formatted_data)
            connection.commit()

            # The maximum timestamp is the timestamp of the last inserted record
            max_timestamp = formatted_data[0]

            # Delete records beyond 48 hours from the maximum timestamp in the SQLite table
            delete_query = f"DELETE FROM {schema['table']} WHERE datetime(timestamp) < datetime('{max_timestamp}', '-48 hours')"
            cursor.execute(delete_query)
            connection.commit()

            return cursor.lastrowid > 0

    except sqlite3.Error as error_msg:
        print("Error: " + str(error_msg))
        sys.exit()

    finally:
        connection.close()
