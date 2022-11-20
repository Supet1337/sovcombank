import starlette.status

from app.main import app, templates

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, Cookie

import httpx

from app.utility import JAVA_BACK_URL


@app.get("/", response_class=HTMLResponse)
def root(request: Request, vtauth: str | None = Cookie(default=None)):
    from app.main import sessions
    req = httpx.get(f"{JAVA_BACK_URL}/posts")
    if req.status_code == 200:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "is_authorized": True if sessions.check_session(vtauth) is not None else False,
            "posts": req.json()
        })

    else:
        return RedirectResponse(f"/{req.status_code}", status_code=starlette.status.HTTP_302_FOUND)

