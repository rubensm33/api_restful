from pydantic import BaseModel, EmailStr
from typing import List, Optional


class UserBase(BaseModel):
    name: str
    email: EmailStr
    is_active: Optional[bool] = False
    balance: Optional[float] = 10000.0


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    hashed_password: str
    is_active: Optional[bool] = False
    balance: Optional[float] = 10000.0


class UserForm(BaseModel):
    name: str
    email: EmailStr
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
