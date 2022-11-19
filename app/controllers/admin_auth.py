import starlette.status

from app.controllers.auth import update_sessions
from app.main import app, templates, sessions
from app.utility import gen_token, hash_password, JAVA_BACK_URL, COOKIE_TOKEN_KEY

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, Form

import httpx


@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login(request: Request, q: str | None = None):
    errors: list = []
    if q is not None:
        if q == "notauthorized":
            errors.append("Вы не имеете доступа к этой странице! Авторизируйтесь!")

    return templates.TemplateResponse("auth/admin/login.html",
                                      {
                                          "request": request,
                                          "errors": errors
                                      })


@app.post("/admin/login")
async def admin_login(
        request: Request,
        email: str = Form(), password: str = Form()
        ):

    hashed_password = hash_password(password)
    check = httpx.post(JAVA_BACK_URL, json={
        "email": email,
        "password": hashed_password
    })

    if check.status_code == 404:
        return templates.TemplateResponse("auth/admin/login.html",
                                          {
                                              "request": request,
                                              "errors": ["Неверная почта или пароль!"]
                                          })
    elif check.status_code == 200:
        response = RedirectResponse("/admin", status_code=starlette.status.HTTP_302_FOUND)
        response.set_cookie(**update_sessions(request, email))
        return response


@app.get("/register", response_class=HTMLResponse)
async def admin_register(request: Request):
    return templates.TemplateResponse("auth/admin/register.html",
                                      {
                                          "request": request
                                      })


@app.post("/register")
async def admin_register(request: Request,
                         name: str = Form(), email: str = Form(), password: str = Form(), confirm_password: str = Form(),
                         code: str = Form()
                         ):
    if not password == confirm_password:
        return templates.TemplateResponse("auth/admin/register.html",
                                          {
                                              "request": request,
                                              "errors": ["Пароли не совпадают"]
                                          })
    hashed_password = hash_password(password)

    check = httpx.post(JAVA_BACK_URL, json={
        "email": email,
        "name": name,
        "password": hashed_password,
        "code": code
    })

    if check.status_code == 403 or check.status_code == 409:
        return templates.TemplateResponse("auth/admin/register.html",
                                          {
                                              "request": request,
                                              "errors": ["Такого кода приглашения не существует!"
                                                         if check.status_code == 403
                                                         else "Такой администратор уже существует!"]
                                          })
    elif check.status_code == 200:
        response = RedirectResponse("/admin", status_code=starlette.status.HTTP_302_FOUND)
        response.set_cookie(**update_sessions(request, email, True))
        return response
