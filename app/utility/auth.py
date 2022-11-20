import functools
import hashlib
import httpx

from fastapi import Request

from . import JAVA_BACK_URL, SECRET_KEY, COOKIE_TOKEN_KEY
from app.schemas import UserData


def hash_password(password: str) -> str:
    h = hashlib.new('sha256')
    h.update(f"{password}|{SECRET_KEY}".encode('UTF-8'))
    return h.hexdigest()


def gen_token(client_ip: str, email: str) -> str:
    """
    Generating token for validating session in cookies
    :param client_ip: IP to pin session to user's IP
    :param email: User's email to identify
    :return: Generated session token to put it in cookies
    """
    h = hashlib.new('sha256')
    h.update(f"{client_ip}|{email}|{SECRET_KEY}".encode('UTF-8'))
    return h.hexdigest()


def check_token(client_ip: str, email: str, token: str) -> bool:
    __token = gen_token(client_ip, email)
    return token == __token


def check_user(email: str) -> UserData | None:
    req = httpx.post(JAVA_BACK_URL, json={"email": email})
    if req.status_code == 200: UserData(**req.json())
    elif req.status_code == 404: return None


def update_sessions(request: Request, email: str, is_admin: bool = False) -> dict:
    client_ip = request.client.host
    token = gen_token(client_ip, email)

    from app.main import sessions
    sessions.add_session(token, email, client_ip, is_admin)
    return {
        "key": COOKIE_TOKEN_KEY,
        "value": token,
        "httponly": True,
        "max_age": 60 * 60
    }


def check_auth(cookie_token: str | None) -> str | None:
    from app.main import sessions
    if cookie_token is not None:
        session = sessions.check_session(cookie_token)
        if session is None: return None
        else: return session.get("email")
    else:
        return None


def get_session(cookie_token: str | None) -> dict | None:
    from app.main import sessions
    if cookie_token is not None:
        return sessions.check_session(cookie_token)


def are_null_strings(*args: list[str]) -> bool:
    for string in args:
        if string == "" or string is None:
            return False
    else:
        return True
