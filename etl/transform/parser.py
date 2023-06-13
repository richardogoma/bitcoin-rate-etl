from datetime import datetime
from decimal import Decimal


def parse_dict(data: dict) -> list:
    timestamp_str = data["time"]["updatedISO"]
    timestamp = datetime.fromisoformat(timestamp_str)

    usd_rate = Decimal(data["bpi"]["USD"]["rate_float"]).quantize(Decimal("0.0000"))
    gbp_rate = Decimal(data["bpi"]["GBP"]["rate_float"]).quantize(Decimal("0.0000"))
    eur_rate = Decimal(data["bpi"]["EUR"]["rate_float"]).quantize(Decimal("0.0000"))

    chart_name = str(data["chartName"])

    parsed_data = [timestamp, chart_name, usd_rate, gbp_rate, eur_rate]
    return parsed_data
