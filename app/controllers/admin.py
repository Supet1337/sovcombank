import httpx
import starlette.status

from app.main import app, templates
from app.utility import get_session, JAVA_BACK_URL

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, Cookie, Form


@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request, vtauth: str | None = Cookie(default=None)):
    session = get_session(vtauth)
    if session is None: return RedirectResponse("/", status_code=starlette.status.HTTP_302_FOUND)
    if not session.get("is_admin"): return RedirectResponse("/403", status_code=starlette.status.HTTP_302_FOUND)

    req = httpx.get(f"{JAVA_BACK_URL}/admins/confirmation")

    if req.status_code == 200:
        users = req.json()
        return templates.TemplateResponse("/user/admin.html",
                                          {"request": request,
                                           "users": users,
                                           "is_admin": True
                                           })


@app.post("/admin/ban")
async def ban_user(request: Request, vtauth: str | None = Cookie(default=None),
                   email: str = Form()):
    session = get_session(vtauth)
    if session is None: return RedirectResponse("/", status_code=starlette.status.HTTP_302_FOUND)
    if not session.get("is_admin"): return RedirectResponse("/403", status_code=starlette.status.HTTP_302_FOUND)

    req = httpx.put(JAVA_BACK_URL + "/admins/banned",
                    json={
                        "banned": True,
                        "userEmail": email
                    })

    if req.status_code == 200:
        return RedirectResponse("/admin", status_code=starlette.status.HTTP_302_FOUND)


@app.post("/admin/approve")
async def ban_user(request: Request, vtauth: str | None = Cookie(default=None),
                   email: str = Form()):
    session = get_session(vtauth)
    if session is None: return RedirectResponse("/", status_code=starlette.status.HTTP_302_FOUND)
    if not session.get("is_admin"): return RedirectResponse("/403", status_code=starlette.status.HTTP_302_FOUND)

    req = httpx.put(JAVA_BACK_URL + "/admins/confirmation",
                    json={
                        "email": email
                    })

    if req.status_code == 200:
        return RedirectResponse("/admin", status_code=starlette.status.HTTP_302_FOUND)
