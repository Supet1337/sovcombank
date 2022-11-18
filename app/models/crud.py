from sqlalchemy.orm import Session

from .project import *
from .posts import *


def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


def get_project_by_title(db: Session, project_title: str):
    return db.query(Project).filter(Project.title == project_title).first()


def get_all_projects(db: Session, skip: int = 0, limit: int = 12):
    return db.query(Project).offset(skip).limit(limit).all()


def create_project(db: Session, project: ProjectCreate):
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project


def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


def get_post_by_title(db: Session, post_title: str):
    return db.query(Post).filter(Post.title == post_title).first()


def get_all_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).order_by(-Post.id).offset(skip).limit(limit).all()


def create_post(db: Session, post: PostCreate):
    db_post = Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post
