from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    is_active: Optional[bool] = True
    balance: Optional[float] = 0.0

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_active: Optional[bool]
    balance: Optional[float]