from app.main import app, templates, sessions

from fastapi.responses import HTMLResponse
from fastapi import Request


@app.get("/user", response_class=HTMLResponse)
async def user(request: Request):
    return templates.TemplateResponse("user/user.html",
                                      {
                                          "request": request
                                      })
