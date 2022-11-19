from app.main import app, templates

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, Cookie

from app.utility import CurrencyDescriptionDict


@app.get("/user", response_class=HTMLResponse)
async def user(request: Request, vtauth: str | None = Cookie(default=None)):
    if vtauth is None:
        return RedirectResponse("/login?q=notauthorized")

    return templates.TemplateResponse("user/user.html",
                                      {
                                          "request": request,
                                          "currency_dict": CurrencyDescriptionDict
                                      })

