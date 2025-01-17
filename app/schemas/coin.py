from pydantic import BaseModel


class CoinBase(BaseModel):
    name: str
    price: float
    volume_24h: float
    quantity: int
    percent_change_1h: float
    percent_change_24h: float
    percent_change_7d: float


class CoinResponse(CoinBase):
    id: int

    class Config:
        orm_mode = True


class CoinAverage(BaseModel):
    user_id: int
    average_price: float
    name: str
    quantity: int

    class Config:
        orm_mode = True
