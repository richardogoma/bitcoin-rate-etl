from etl.load.loader import load_data
from config import Config
import pytest
from datetime import datetime
from decimal import Decimal


@pytest.fixture
def test_data_fixture():
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
    test_data = test_data_fixture
    result = load_data(Config.DATABASE_URI, test_data)
    assert True == result


# Test data insertion with conflict resolution
def test_conflict_resolution(conflict_test_data_fixture):
    test_data = conflict_test_data_fixture
    result = load_data(Config.DATABASE_URI, test_data)
    assert False == result
