""" Extraction logic """
import requests


def retrieve_rates(uri: str) -> dict:
    """
    Retrieves Bitcoin rates from a specified URI.

    Args:
        uri (str): The URI to retrieve the rates from.

    Returns:
        dict: The deserialized JSON response containing the rates.
    """
    response = requests.request("GET", uri, timeout=60)
    if response.status_code == 200:
        deserialized_response = response.json()
        return deserialized_response

    return {}
