import httpx
import starlette.status

from app.main import app
from app.schemas.enums import OperationEnum
from app.utility import JAVA_BACK_URL, check_auth, get_currency

from fastapi import Request, Cookie, Form
from fastapi.responses import RedirectResponse


@app.post("/deal")
async def make_deal(request: Request, vtauth: str | None = Cookie(default=None),
                    operation: OperationEnum = Form(default=OperationEnum.buy),
                    account_id: int = Form(), currency_key: str = Form(), number: float = Form()):
    errors = []
    s_email = check_auth(vtauth)
    if s_email is None: return RedirectResponse("/login?q=notauthorized", status_code=starlette.status.HTTP_302_FOUND)
    currency_ratio = sum(get_currency(currency_key, 0))

    opres = httpx.post(f"{JAVA_BACK_URL}/deal/accounts?email={s_email}",
                       json={
                           "accountId": account_id,
                           "currencyRatio": currency_ratio,
                           "sum": -number if operation == OperationEnum.buy else number
                       })
    if opres.status_code == 402:
        return RedirectResponse("/402")
    if opres.status_code == 200:
        return RedirectResponse("/user", status_code=starlette.status.HTTP_302_FOUND)
    else:

        return RedirectResponse("/", status_code=starlette.status.HTTP_302_FOUND)
