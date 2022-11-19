import starlette.status

from app.main import app, templates, sessions
from app.utility import gen_token, hash_password, JAVA_BACK_URL, COOKIE_TOKEN_KEY

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, Form

import httpx


# Отображаем страницу для логина
@app.get("/login", response_class=HTMLResponse)
async def login(
        request: Request, q: str | None = None
):
    errors: list = []
    if q is not None:
        if q == "notauthorized":
            errors.append("Вы не имеете доступа к этой странице! Авторизируйтесь!")

    return templates.TemplateResponse("auth/login.html",
                                      {
                                          "request": request,
                                          "errors": errors
                                      })


# Получаем данные с форм и редиректим если всё ок
@app.post("/login")
async def login(
        request: Request,
        email: str = Form(), password: str = Form(),
):
    hashed_password: str = hash_password(password)

    check = httpx.post(JAVA_BACK_URL, json={
        "email": email,
        "password": hashed_password
    })

    if check.status_code == 404:
        return templates.TemplateResponse("auth/login.html",
                                          {
                                              "request": request,
                                              "errors": ["Неверная почта или пароль!"]
                                          })
    elif check.status_code == 200:
        # Записываем токен сессии в куки
        response = RedirectResponse("/user", status_code=starlette.status.HTTP_302_FOUND)
        response.set_cookie(**update_sessions(request, email))
        return response


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
    # Validate data
    if not password == confirm_password:
        return templates.TemplateResponse("auth/register.html",
                                          {
                                              "request": request,
                                              "errors": ["Пароли не совпадают!"]
                                          })

    hashed_password = hash_password(password)

    check = httpx.post(JAVA_BACK_URL, json={
        "email": email,
        "fullname": fullname,
        "password": hashed_password
    })

    if check.status_code == 409:
        return templates.TemplateResponse("auth/register.html",
                                          {
                                              "request": request,
                                              "errors": ["Такой администратор уже существует!"]
                                          })
    elif check.status_code == 200:
        response = RedirectResponse("/user", status_code=starlette.status.HTTP_302_FOUND)
        response.set_cookie(**update_sessions(request, email))
        return response


def update_sessions(request: Request, email: str, is_admin: bool = False) -> dict:
    client_ip = request.client.host
    token = gen_token(client_ip, email)
    sessions.add_session(token, email, client_ip, is_admin)
    return {
        "key": COOKIE_TOKEN_KEY,
        "value": token,
        "httponly": True,
        "max_age": 60 * 60
    }


