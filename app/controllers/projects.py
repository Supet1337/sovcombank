from sqlalchemy.orm import Session
from fastapi import Request, Depends, Form
from fastapi.responses import HTMLResponse

from app.models import crud, ProjectCreate
from app.main import app, templates, get_db
from app.utility import ADMIN_KEY


@app.get("/projects", response_class=HTMLResponse)
def projects_page(request: Request, admin_key: str = '', db: Session = Depends(get_db)):
    projects = crud.get_all_projects(db)
    return templates.TemplateResponse("projects.html",
                                      {"request": request,
                                       "title": "Projects",
                                       "is_admin": admin_key == ADMIN_KEY,
                                       "projects": projects
                                       })


@app.post("/projects")
def projects_page(
        request: Request,
        title: str = Form(), image_path: str = Form(), git_link: str = Form(), description: str = Form(),
        db: Session = Depends(get_db)
        ):

    if not crud.get_project_by_title(db, title):
        db_project = ProjectCreate(title=title, description=description, git_link=git_link, image_path=image_path)
        crud.create_project(db, db_project)

        projects = crud.get_all_projects(db)
        return templates.TemplateResponse("projects.html",
                                          {"request": request,
                                           "title": "Projects",
                                           "is_admin": True,
                                           "projects": projects
                                           })
    else:
        return templates.TemplateResponse("404.html",
                                          {"request": request
                                           })
