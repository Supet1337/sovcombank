from pydantic import BaseModel
from .account import AccountData


class UserRegister(BaseModel):
    fullname: str
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Иванов Иван Иванович",
                "email": "ivanov@example.com",
                "password": "hashed password"
            }
        }


class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "ivanov@example.com",
                "password": "hashed password"
            }
        }


class UserData(BaseModel):
    fullname: str
    is_banned: bool
    accounts: list[AccountData]
