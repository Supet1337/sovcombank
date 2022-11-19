from app.main import app, templates

from fastapi import Request
from fastapi.responses import HTMLResponse


@app.get("/account/{account_id}", response_class=HTMLResponse)
async def account_page(request: Request, account_id: int):
    errors = []
    # validate id or redirect to 404
    # send {email, account_id} and get information and validation
    return templates.TemplateResponse("user/account.html",
                                      {
                                          "request": request,
                                          "errors": errors
                                      })
