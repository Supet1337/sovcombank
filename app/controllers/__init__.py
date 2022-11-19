from .base import app
from .auth import app
from .errorshandlers import app
from .user import app
from .admin_auth import app

__all__ = ['app']
