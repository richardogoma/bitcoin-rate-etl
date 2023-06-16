"""
Test data loading logic.
"""

from datetime import datetime
from decimal import Decimal
import pytest
from etl.load.loader import load_data
from config import Config


@pytest.fixture
def test_data_fixture():
    """
    Fixture that returns test data for data loading.

    Returns:
        list: The test data in the format [timestamp, chart_name, usd_rate, gbp_rate, eur_rate].
    """
    timestamp = datetime.fromisoformat("1900-01-01T15:22:00+00:00")

    data = [
        timestamp,  # timestamp
        "Test",  # chart_name
        Decimal("25623.6857"),  # usd_rate
        Decimal("21410.9468"),  # gbp_rate
        Decimal("24961.211"),  # eur_rate
    ]
    return data


@pytest.fixture
def conflict_test_data_fixture():
    """
    Fixture that returns conflicting test data for data loading.

    Returns:
        list: The conflicting test data in the format
            [timestamp, chart_name, usd_rate, gbp_rate, eur_rate].
    """
    timestamp = datetime.fromisoformat("1900-01-01T15:22:00+00:00")

    data = [
        timestamp,  # timestamp
        "Test",  # chart_name
        Decimal("25644.1739"),  # usd_rate
        Decimal("21428.0665"),  # gbp_rate
        Decimal("24981.1694"),  # eur_rate
    ]
    return data


def test_data_loading(test_data_fixture):
    """
    Test the data loading function.

    It verifies that data is successfully loaded into the database.

    Args:
        test_data_fixture (list): Test data in the format
            [timestamp, chart_name, usd_rate, gbp_rate, eur_rate].
    """
    test_data = test_data_fixture
    result = load_data(Config.DATABASE_URI, test_data)
    assert True is result


def test_conflict_resolution(conflict_test_data_fixture):
    """
    Test data insertion with conflict resolution.

    It verifies that conflicting data is correctly handled during insertion.

    Args:
        conflict_test_data_fixture (list): Conflict test data in the format
            [timestamp, chart_name, usd_rate, gbp_rate, eur_rate].
    """
    test_data = conflict_test_data_fixture
    result = load_data(Config.DATABASE_URI, test_data)
    assert False is result
