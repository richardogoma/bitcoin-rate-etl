from etl.extract.retriever import retrieve_rates
from config import Config


def test_retrieve_rates():
    result = retrieve_rates(uri=Config.API_URI)

    assert "time" in result
