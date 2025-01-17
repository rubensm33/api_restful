from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from schemas import user as user_schema
from repositories import user_repository

from config.database import get_db


router = APIRouter(prefix="/users")


@router.post("/", response_model=user_schema.UserResponse)
def create_user(user: user_schema.UserForm, db: Session = Depends(get_db)):

    user_create = user_schema.UserCreate(name=user.name, email=user.email, hashed_password=user.password)
    db_user = user_repository.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registrated")

    db_user = user_repository.create_user(db=db, user_data=user_create)

    return user_schema.UserResponse.model_validate(db_user, from_attributes=True)
