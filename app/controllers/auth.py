from app.main import app, templates, sessions
from app.utility import gen_token

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, Form


# Отображаем страницу для логина
@app.get("/login", response_class=HTMLResponse)
async def login(
        request: Request
        ):
    return templates.TemplateResponse("auth/login.html",
                                      {
                                          "request": request,
                                          "sessions": sessions
                                      })


# Получаем данные с форм и редиректим если всё ок
@app.post("/login")
async def login(
        request: Request,
        email: str = Form(), password: str = Form()
        ):

    # If successful
    update_sessions(request, email)
    return RedirectResponse("/user")


# Отображаем страницу для регистрации
@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("auth/register.html",
                                      {
                                          "request": request
                                      })


# Получаем данные с форм и редиректим если всё ок
@app.post("/register")
async def register(
        request: Request,
        email: str = Form(), fullname: str = Form(), password: str = Form(), confirm_password: str = Form()
):

    # If successful
    update_sessions(request, email)
    return RedirectResponse("/user")


def update_sessions(request: Request, email: str):
    client_ip = request.client.host
    token = gen_token(client_ip, email)
    request.cookies["__vtauth"] = token
    sessions.add_session(token, email, client_ip)

