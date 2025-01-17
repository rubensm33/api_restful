from datetime import datetime
from pydantic import BaseModel


class TransactionCreate(BaseModel):
    coin_name: str
    quantity: float


class TransactionResponse(BaseModel):
    id: int
    user_id: int
    coin_name: str
    quantity: float
    total_price: float
    transaction_type: str
    transaction_date: datetime

    class Config:
        orm_mode = True


class TransactionSell(BaseModel):
    coin_name: str
    coin_id: int
    quantity: float
