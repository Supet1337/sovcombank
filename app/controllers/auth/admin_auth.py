import starlette.status

from app.main import app, templates
from app.utility import hash_password, JAVA_BACK_URL, update_sessions, EMPTY_FORMS_MESSAGE, WRONG_PASSWORD, \
    PASSWORDS_DONT_MATCH, ADMIN_KEY_NOT_FOUND, USER_EXISTS

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

    errors = []
    if email == "" or password == "": errors.append(EMPTY_FORMS_MESSAGE)

    hashed_password = hash_password(password)
    check = httpx.post(JAVA_BACK_URL + "/admins/login", json={
        "email": email,
        "password": hashed_password
    })

    if check.status_code == 404: errors.append(WRONG_PASSWORD)

    if len(errors):
        return templates.TemplateResponse("auth/admin/login.html",
                                          {
                                              "request": request,
                                              "errors": errors
                                          })
    elif check.status_code == 200:
        response = RedirectResponse("/admin", status_code=starlette.status.HTTP_302_FOUND)
        response.set_cookie(**update_sessions(request, email, is_admin=True))
        return response


@app.get("/admin/register", response_class=HTMLResponse)
async def admin_register(request: Request):
    return templates.TemplateResponse("auth/admin/register.html",
                                      {
                                          "request": request
                                      })


@app.post("/admin/register")
async def admin_register(request: Request,
                         name: str = Form(), invite_code: str = Form(),
                          email: str = Form(),
                         password: str = Form(), confirm_password: str = Form(),

                         ):
    errors = []
    if not password == confirm_password: errors.append(PASSWORDS_DONT_MATCH)

    hashed_password = hash_password(password)

    check = httpx.post(JAVA_BACK_URL + "/admins/registration", json={
        "email": email,
        "name": name,
        "password": hashed_password,
        "code": invite_code
    })

    if check.status_code == 403: errors.append(ADMIN_KEY_NOT_FOUND)
    elif check.status_code == 409: errors.append(USER_EXISTS)
    if len(errors):
        return templates.TemplateResponse("auth/admin/register.html",
                                          {
                                              "request": request,
                                              "errors": errors
                                          })
    elif check.status_code == 200:
        response = RedirectResponse("/admin", status_code=starlette.status.HTTP_302_FOUND)
        response.set_cookie(**update_sessions(request, email, is_admin=True))
        return response
