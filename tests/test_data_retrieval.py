"""
Test data extraction logic.
"""

from etl.extract.retriever import retrieve_rates
from config import Config


def test_retrieve_rates():
    """
    Test the retrieve_rates function.

    It verifies that the retrieve_rates function returns a result containing the "time" key.
    """
    result = retrieve_rates(uri=Config.API_URI)

    assert "time" in result
