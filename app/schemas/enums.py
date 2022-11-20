from enum import Enum


class CurrencyEnum(str, Enum):
    Usd = "USD"
    Eur = "EUR"
    Jpy = "JPY"
    Gbp = "GBP"
    Aud = "AUD"
    Cad = "CAD"
    Chf = "CHF"
    Cny = "CNY"
    Sek = "SEK"
    Mxn = "MXN"
    Nzd = "NZD"
    Sgd = "SGD"
    Hkd = "HKD"
    Nok = "NOK"
    Krw = "KRW"
    Try = "TRY"
    Inr = "INR"
    Brl = "BRL"
    Zar = "ZAR"
    Dkk = "DKK"
    Pln = "PLN"
    Twd = "TWD"
    Thb = "THB"
    Myr = "MYR"


class OperationEnum(str, Enum):
    buy = "buy"
    sell = "sell"


class BalanceOperationEnum(str, Enum):
    insert = "insert"
    withdraw = "withdraw"
