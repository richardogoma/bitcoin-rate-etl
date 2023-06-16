"""
Test data transformation logic.
"""

import json
from datetime import datetime
from decimal import Decimal
import pytest
from etl.transform.parser import parse_dict


@pytest.fixture
def test_file_path():
    """
    Fixture that returns the file path for test data.
    """
    return "./data/raw/sample.json"


def read_json_file(file_path):
    """
    Read and deserialize JSON data from a file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The deserialized JSON data.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        json_data = file.read()
        deserialized_data = json.loads(json_data)
    return deserialized_data


def test_data_parsing(test_file_path):
    """
    Test the data parsing function.

    It verifies that the parsed data has the expected types and values.
    """
    test_data = read_json_file(test_file_path)
    result = parse_dict(test_data)

    assert isinstance(result[0], datetime)
    assert "Bitcoin" in result[1]
    assert isinstance(result[4], Decimal)
