from pydantic import BaseModel


class AccountData(BaseModel):
    id: int
    currency_key: str
    balance: float

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "currency_key": "RUB",
                "balance": 100.0
            }
        }
