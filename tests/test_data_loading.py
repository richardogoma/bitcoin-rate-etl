from etl.load.loader import load_data
from config import Config
import pytest
from datetime import datetime
from decimal import Decimal


@pytest.fixture
def test_data_fixture():
    data = [
        datetime.now(),  # timestamp
        "Test",  # chart_name
        Decimal("50000.1234"),  # usd_rate
        Decimal("40000.5678"),  # gbp_rate
        Decimal("45000.7890"),  # eur_rate
    ]
    return data


def test_data_loading(test_data_fixture):
    test_data = test_data_fixture
    result = load_data(Config.DATABASE_URI, test_data)
    assert True == result
