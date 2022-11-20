import httpx
import starlette.status

from app.main import app
from app.schemas.enums import CurrencyEnum
from app.utility import JAVA_BACK_URL, check_auth

from fastapi import Request, Cookie, Form
from fastapi.responses import RedirectResponse


@app.get("/account/{account_id}")
async def account_page(request: Request, account_id: int, vtauth: str | None = Cookie(default=None)):
    errors = []
    s_email = check_auth(vtauth)
    if s_email is None: return RedirectResponse("/login?q=notauthorized", status_code=starlette.status.HTTP_302_FOUND)
    check = httpx.post(JAVA_BACK_URL + "/accounts/account/check",
                       json={
                           "accountId": account_id,
                           "email": s_email
                       })
    if check.status_code == 403: return RedirectResponse("/user", status_code=starlette.status.HTTP_302_FOUND)
    elif check.status_code == 404: return RedirectResponse("/404", status_code=starlette.status.HTTP_302_FOUND)
    elif check.status_code == 200:
        response = RedirectResponse(f"/user?id={account_id}",
                                    status_code=starlette.status.HTTP_302_FOUND)

        return response


@app.post("/account/create")
async def create_account(request: Request, vtauth: str | None = Cookie(default=None),
                         new_bill_val: CurrencyEnum = Form(default=CurrencyEnum.Usd)
                         ):
    errors = []
    s_email = check_auth(vtauth)
    if s_email is None: return RedirectResponse("/login?q=notauthorized", status_code=starlette.status.HTTP_302_FOUND)

    check = httpx.post(JAVA_BACK_URL + "/accounts/create", json={
        "currency": new_bill_val,
        "email": s_email
    })
    if check.status_code == 200: return RedirectResponse("/user", status_code=starlette.status.HTTP_302_FOUND)


@app.post("/changepredict")
async def change_prediction(request: Request,
                            predict_currency: CurrencyEnum = Form(default=CurrencyEnum.Usd)):

    return RedirectResponse(f"/user?pc={predict_currency}", status_code=starlette.status.HTTP_302_FOUND)
