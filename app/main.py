from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.utility import STATIC_FILES_PATH, TEMPLATES_PATH, SessionsContainer

templates = Jinja2Templates(directory=TEMPLATES_PATH)

app = FastAPI()
app.mount(f"/{STATIC_FILES_PATH}", StaticFiles(directory=STATIC_FILES_PATH), name="static")

# token: {email, ip}
sessions = SessionsContainer()

# Importing to use controllers from another package
from app.controllers import app

