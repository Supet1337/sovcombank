from sqlalchemy import Column, Integer, String
from pydantic import BaseModel

from app.database import Base


class JProjectBase(BaseModel):
    title: str
    description: str
    git_link: str
    image_path: str


class ProjectCreate(JProjectBase):
    pass


class ProjectJSON(JProjectBase):
    id: int

    class Config:
        orm_mode = True


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    description = Column(String)
    git_link = Column(String)
    image_path = Column(String)
