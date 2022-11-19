from app.main import app, templates, sessions

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, Cookie

from app.utility import COOKIE_TOKEN_KEY


@app.get("/user", response_class=HTMLResponse)
async def user(request: Request, vtauth: str | None = Cookie(default=None)):
    if vtauth is None:
        return RedirectResponse("/login")

    return templates.TemplateResponse("user/user.html",
                                      {
                                          "request": request
                                      })
