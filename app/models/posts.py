from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from pydantic import BaseModel

from datetime import datetime

from app.database import Base


class JPostBase(BaseModel):
    title: str
    content: str
    image_path: str
    date: datetime = datetime.now()


class PostCreate(JPostBase):
    pass


class PostJSON(JPostBase):
    id: int

    class Config:
        orm_mode = True


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    content = Column(String)
    image_path = Column(String)
    date = Column(DateTime(timezone=True), server_default=func.now())
