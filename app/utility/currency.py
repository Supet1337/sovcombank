from datetime import date, timedelta

import httpx

BASE = "RUB"


def get_currency(currency_key: str = "USD", days: int = 7) -> list:
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    url = f'https://api.apilayer.com/fixer/timeseries?start_date={start_date}&end_date={end_date}&base={BASE}&symbols={currency_key} '
    headers = {"apikey": "bNpxciduvfYcvmP4dqyrSXPGQZwDpCkU"}

    response = httpx.get(url, headers=headers)
    raw_data = response.json().get('rates')
    currency = [rate["USD"] for rate in raw_data.values()]
    return currency
