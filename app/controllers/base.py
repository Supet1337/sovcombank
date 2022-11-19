from app.main import app, templates

from fastapi.responses import HTMLResponse
from fastapi import Request, Cookie


@app.get("/", response_class=HTMLResponse)
def root(request: Request, vtauth: str | None = Cookie(default=None)):
    from app.main import sessions
    return templates.TemplateResponse("index.html", {
        "request": request,
        "is_authorized": True if sessions.check_session(vtauth) is not None else False
    })


