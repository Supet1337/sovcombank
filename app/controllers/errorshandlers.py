import starlette.status

from app.main import app, templates

from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from fastapi.responses import HTMLResponse
from fastapi import Request


@app.exception_handler(StarletteHTTPException)
async def redirect_error(request: Request, exception: StarletteHTTPException):
    if exception.status_code == 404:
        return RedirectResponse("/404", starlette.status.HTTP_302_FOUND)


@app.get("/404", response_class=HTMLResponse)
async def handler_404(request: Request):

    return templates.TemplateResponse("errors/404.html", {
        "request": request
    })


@app.get("/401", response_class=HTMLResponse)
async def handler_401(request: Request):
    return templates.TemplateResponse("errors/401.html",
                                      {
                                          "request": request
                                      })


@app.get("/402", response_class=HTMLResponse)
async def handler_402(request: Request):
    return templates.TemplateResponse("errors/402.html",
                                      {
                                          "request": request
                                      })


@app.get("/403", response_class=HTMLResponse)
async def handler_403(request: Request):
    return templates.TemplateResponse("errors/403.html",
                                      {
                                          "request": request
                                      })
