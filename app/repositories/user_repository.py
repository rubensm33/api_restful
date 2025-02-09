from sqlalchemy.orm import Session

from schemas import user
from models import user as user_model, scopes as scopes_model
from services.token_service import hash_password


def get_user(db: Session, user_id: int):
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(user_model.User).filter(user_model.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(user_model.User).offset(skip).limit(limit).all()


def create_user(db: Session, user_data: user.UserCreate):
    user_data.hashed_password = hash_password(user_data.hashed_password)
    user_data_dict = user_data.dict()
    db_user = user_model.User(**user_data_dict)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    db_user = get_user_by_email(db, user_data.email)

    db_scope = scopes_model.UserScopes(user_id=db_user.id, scope="me")
    db.add(db_scope)
    db.commit()
    db.refresh(db_scope)
    return db_user
