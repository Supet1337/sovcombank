import hashlib

import httpx

from . import JAVA_BACK_URL, SECRET_KEY
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
