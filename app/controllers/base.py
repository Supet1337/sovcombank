from app.main import app, templates
from app.utility import ADMIN_KEY

from fastapi.responses import HTMLResponse
from fastapi import Request


@app.get("/", response_class=HTMLResponse)
def root(request: Request, admin_key: str = ''):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "is_admin": admin_key == ADMIN_KEY,
    })


