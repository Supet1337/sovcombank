from app.main import app, templates, sessions
from app.utility import gen_token, hash_password, JAVA_BACK_URL, COOKIE_TOKEN_KEY

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, Form, Response

import httpx


# Отображаем страницу для логина
@app.get("/login", response_class=HTMLResponse)
async def login(
        request: Request
):
    return templates.TemplateResponse("auth/login.html",
                                      {
                                          "request": request
                                      })


# Получаем данные с форм и редиректим если всё ок
@app.post("/login", response_class=HTMLResponse)
async def login(
        request: Request, response: HTMLResponse,
        email: str = Form(), password: str = Form(),
):
    hashed_password = hash_password(password)

    # httpx.post(JAVA_BACK_URL, json={
    #     "email": email,
    #     "password": hashed_password
    # })
    # If successful
    update_sessions(request, email, response)
    return templates.TemplateResponse("user/user.html",
                                      {
                                          "request": request,
                                          "sessions": sessions
                                      })


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
        request: Request, response: HTMLResponse,
        email: str = Form(), fullname: str = Form(), password: str = Form(), confirm_password: str = Form()
):
    # Validate data
    if not password == confirm_password:
        return templates.TemplateResponse("auth/register.html",
                                          {
                                              "request": request,
                                              "errors": ["Пароли не совпадают!"]
                                          })

    hashed_password = hash_password(password)
    httpx.post(JAVA_BACK_URL, json={
        "email": email,
        "fullname": fullname,
        "password": hashed_password
    })

    update_sessions(request, email, response)
    return templates.TemplateResponse("user/user.html",
                                      {
                                          "request": request,
                                          "sessions": sessions
                                      })


def update_sessions(request: Request, email: str, response: Response):
    client_ip = request.client.host
    token = gen_token(client_ip, email)
    response.set_cookie(key=COOKIE_TOKEN_KEY, value=token, httponly=True, max_age=60*60)
    sessions.add_session(token, email, client_ip)
