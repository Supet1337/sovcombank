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


CurrencyDescriptionDict = {
    "USD": "Доллар",
    "EUR": "Евро",
    "JPY": "Японская иена",
    "GBP": "Фунт стерлингов",
    "AUD": "Австралийский доллар",
    "CAD": "Канадский доллар",
    "CHF": "Швейцарский франк",
    "CNY": "Китайский юань",
    "SEK": "Шведская крона",
    "MXN": "Мексиканский песо",
    "NZD": "Новозеландский доллар",
    "SGD": "Сингапурский доллар",
    "HKD": "Гонконгский доллар",
    "NOK": "Норвежская крона",
    "KRW": "Южнокорейская вона",
    "TRY": "Турецкая лира",
    "INR": "Индийская рупия",
    "BRL": "Бразильский реал",
    "ZAR": "Южноафриканский рэнд",
    "DKK": "Датская крона",
    "PLN": "Польский злотый",
    "TWD": "Новый тайваньский доллар",
    "THB": "Тайский бат",
    "MYR": "Малайзийский ринггит"
}

STATIC_FILES_PATH = "app/static"
TEMPLATES_PATH = "app/templates"
SECRET_KEY = '5ba09ea177553a4006e2c33b279ecf559c90face2e3557d5d1cb566884395081'

JAVA_BACK_URL = "http://25.1.212.255:8080"
COOKIE_TOKEN_KEY = "vtauth"
EXCHANGE_APP_ID = '325837b084a644f08a66da6608adf398'
