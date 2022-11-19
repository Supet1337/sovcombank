from app.main import app, templates

from fastapi.responses import HTMLResponse
from fastapi import Request


@app.get("/", response_class=HTMLResponse)
def root(request: Request):

    return templates.TemplateResponse("index.html", {
        "request": request
    })


