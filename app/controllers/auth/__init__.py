from .auth import app
from .admin_auth import app

import starlette.status
from fastapi import Request, Response, Cookie
from fastapi.responses import RedirectResponse
from app.utility import COOKIE_TOKEN_KEY


@app.get("/logout")
async def logout(request: Request,   vtauth: str | None = Cookie(default=None)):
    if vtauth is None: return RedirectResponse("/", status_code=starlette.status.HTTP_302_FOUND)

    from app.main import sessions
    sessions.delete_session(vtauth)
    response = RedirectResponse("/", status_code=starlette.status.HTTP_302_FOUND)
    response.delete_cookie(key=COOKIE_TOKEN_KEY)

    return response

__all__ = ['app']
