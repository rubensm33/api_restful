from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
import jwt

from schemas import user as user_schema
from repositories import user_repository
from config.database import get_db
from utils.constants import *
from services.email_service import send_email
from utils.email_templates import register_email_template

router = APIRouter(prefix="/users")


@router.post("/", response_model=user_schema.UserResponse)
def create_user(user: user_schema.UserForm, db: Session = Depends(get_db)):

    user_create = user_schema.UserCreate(name=user.name, email=user.email, hashed_password=user.password)
    db_user = user_repository.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registrated")

    db_user = user_repository.create_user(db=db, user_data=user_create)

    validation_token = jwt.encode({"email": user.email}, SECRET_KEY, algorithm=ALGORITHM)
    validation_link = f"http://127.0.0.1:8000/users/validate?token={validation_token}"

    content = register_email_template(user.name, validation_link)
    send_email(user.email, "Validação de Email", content)
    return user_schema.UserResponse.model_validate(db_user, from_attributes=True)


@router.get("/validate")
def validate_user(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="Invalid token")

        user = user_repository.get_user_by_email(db, email=email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.is_active:
            return {"message": "User is already active"}

        user.is_active = True
        db.add(user)
        db.commit()
        db.refresh(user)

        return {"message": "User validated successfully"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")
