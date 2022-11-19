import httpx
import starlette.status

from app.main import app, templates
from app.schemas import AccountData
from app.utility import JAVA_BACK_URL, check_auth

from fastapi import Request, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse


@app.get("/account/{account_id}", response_class=HTMLResponse)
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
        account = AccountData(**check.json())
        # TODO: get data for charts through currency key
        return templates.TemplateResponse("user/account.html",
                                          {
                                              "request": request,
                                              "errors": errors,
                                              "account": account
                                          })


@app.get("/account/create")
async def create_account(request: Request):
    errors = []
    # validate data

    return RedirectResponse("/")
