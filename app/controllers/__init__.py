from .base import app
from .errorshandlers import app
from .user import app
from .admin import app

from .auth import app
from .account import app

__all__ = ['app']
