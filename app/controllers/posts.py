from sqlalchemy.orm import Session
from fastapi import Request, Depends, Form
from fastapi.responses import HTMLResponse

from datetime import datetime

from app.models import crud, PostCreate
from app.main import app, templates, get_db
from app.utility import ADMIN_KEY


@app.get("/blog", response_class=HTMLResponse)
def posts_page(request: Request, admin_key: str = '', db: Session = Depends(get_db)):
    posts = crud.get_all_posts(db)
    return templates.TemplateResponse("posts.html",
                                      {"request": request,
                                       "title": "Posts",
                                       "is_admin": admin_key == ADMIN_KEY,
                                       "posts": posts
                                       })


@app.post("/blog", response_class=HTMLResponse)
def posts_page(
                request: Request,
                title: str = Form(), image_path: str = Form(), content: str = Form(),
                db: Session = Depends(get_db)
                ):
    if not crud.get_post_by_title(db, title):
        db_post = PostCreate(title=title, content=content, image_path=image_path)
        crud.create_post(db, db_post)

        posts = crud.get_all_posts(db)

        return templates.TemplateResponse("posts.html",
                                          {
                                              "request": request,
                                              "title": "Blog",
                                              "is_admin": True,
                                              "posts": posts
                                          })
    else:
        return templates.TemplateResponse("404.html",
                                          {
                                              "request": request
                                          })
