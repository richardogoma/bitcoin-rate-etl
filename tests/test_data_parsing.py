from etl.transform.parser import parse_dict
import json
import pytest
from datetime import datetime
from decimal import Decimal


def read_json_file(file_path):
    with open(file_path, "r") as file:
        json_data = file.read()
        deserialized_data = json.loads(json_data)
    return deserialized_data


@pytest.fixture
def file_path():
    return "./data/raw/sample.json"


def test_data_parsing(file_path):
    test_data = read_json_file(file_path)
    result = parse_dict(test_data)

    assert isinstance(result[0], datetime)
    assert "Bitcoin" in result
    assert isinstance(result[4], Decimal)
