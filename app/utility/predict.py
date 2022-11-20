import requests
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

from app.utility import EXCHANGE_APP_ID


def forecast(start_date: str, end_date: str, currency: str):
    """
    Forecast of currency
    :param start_date: Date string in format YYYY-MM-DD
    :param end_date: Date string in format YYYY-MM-DD
    :param currency: Currency key for
    :return:
    """
    base = currency
    symbols = "RUB"

    url = f'https://api.apilayer.com/fixer/timeseries?start_date={start_date}&end_date={end_date}&base={base}&symbols={symbols}'
    payload = {}
    headers = {"apikey": EXCHANGE_APP_ID}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    df = pd.DataFrame.from_dict(data['rates'], orient='index')

    model = ARIMA(list(df[symbols]), order=(4,1,0))
    model_fit = model.fit()
    output = model_fit.forecast()

    return output[0]
