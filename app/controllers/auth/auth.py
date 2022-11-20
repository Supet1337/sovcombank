import starlette.status

from app.main import app, templates
from app.utility import hash_password, JAVA_BACK_URL, update_sessions, WRONG_PASSWORD, PASSWORDS_DONT_MATCH, USER_EXISTS

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

    check = httpx.post(JAVA_BACK_URL + "/login", json={
        "email": email,
        "password": hashed_password
    })

    if check.status_code == 404:
        return templates.TemplateResponse("auth/login.html",
                                          {
                                              "request": request,
                                              "errors": [WRONG_PASSWORD]
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
        first_name: str = Form(), second_name: str = Form(), email: str = Form(), password: str = Form(), confirm_password: str = Form()
):
    # Validate data
    if not password == confirm_password:
        return templates.TemplateResponse("auth/register.html",
                                          {
                                              "request": request,
                                              "errors": [PASSWORDS_DONT_MATCH]
                                          })

    hashed_password = hash_password(password)

    check = httpx.post(JAVA_BACK_URL + "/registration", json={
        "email": email,
        "name": " ".join([first_name, second_name]),
        "password": hashed_password
    })

    if check.status_code == 409:
        return templates.TemplateResponse("auth/register.html",
                                          {
                                              "request": request,
                                              "errors": [USER_EXISTS]
                                          })
    elif check.status_code == 200:
        response = RedirectResponse("/user", status_code=starlette.status.HTTP_302_FOUND)
        response.set_cookie(**update_sessions(request, email))
        return response




