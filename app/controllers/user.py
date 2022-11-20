import datetime
from datetime import date

import httpx

from app.main import app, templates

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, Cookie

from app.utility import CurrencyDescriptionDict, check_auth, JAVA_BACK_URL, forecast, get_currency


@app.get("/user", response_class=HTMLResponse)
async def user(request: Request, id: int | None = None, pc: str | None = None,
               vtauth: str | None = Cookie(default=None)):
    from app.main import sessions
    if sessions.check_session(vtauth) is None:
        return RedirectResponse("/login?q=notauthorized")

    email = check_auth(vtauth)
    accounts: list = httpx.get(f"{JAVA_BACK_URL}/accounts/{email}").json()
    current_account = None

    if id is not None:
        current_account = list(filter(lambda a: a["id"] == id, accounts))[0]
    else:
        current_account = accounts[0]

    week_currency = get_currency(currency_key=current_account.get("currency_key", current_account["currency"]), days=7)
    month_currency = get_currency(currency_key=current_account.get("currency_key", current_account["currency"]),
                                  days=30)

    t_year_currency = get_currency(currency_key=current_account.get("currency_key", current_account["currency"]),
                                   days=365)
    year_currency = [sum(t_year_currency[i:i + 30]) / 30 for i in range(0, 360, 30)]

    return templates.TemplateResponse("user/user.html",
                                      {
                                          "request": request,
                                          "is_authorized": True,
                                          "currency_dict": CurrencyDescriptionDict,
                                          "current_account": current_account,
                                          "accounts": accounts,
                                          "currencies": {
                                              "week": week_currency[::-1],
                                              "month": month_currency[::-1],
                                              "year": year_currency[::-1]
                                          },
                                          "prediction": str(
                                              forecast((date.today() - datetime.timedelta(days=365)).isoformat(),
                                                       date.today().isoformat(),
                                                       pc if pc is not None else "USD"))[:8]

                                      })
