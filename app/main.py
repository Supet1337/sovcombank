from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .database import SessionLocal, engine
from .models import Base
from .utility import *

templates = Jinja2Templates(directory=TEMPLATES_PATH)

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount(f"/{STATIC_FILES_PATH}", StaticFiles(directory=STATIC_FILES_PATH), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Importing to use controllers from another package
from app.controllers import app

