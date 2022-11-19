import httpx

from app.main import app, templates

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, Cookie

from app.utility import CurrencyDescriptionDict, check_auth, JAVA_BACK_URL


@app.post("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    pass
