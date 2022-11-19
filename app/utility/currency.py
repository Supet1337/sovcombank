from datetime import date, timedelta

import httpx

from app.utility import EXCHANGE_APP_ID

BASE = "RUB"


def get_currency(currency_key: str = "USD", days: int = 7) -> list:
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    url = f'https://api.apilayer.com/fixer/timeseries?start_date={start_date}&end_date={end_date}&base={BASE}&symbols={currency_key} '
    headers = {"apikey": EXCHANGE_APP_ID}

    response = httpx.get(url, headers=headers)
    raw_data = response.json().get('rates')
    currency = [rate[currency_key] for rate in raw_data.values()]
    return currency
