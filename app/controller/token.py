from datetime import timedelta
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas.token import Token
from config.database import get_db
from services.user_service import authenticate_user
from services.token_service import create_access_token
from utils.constants import *


router = APIRouter(prefix="/token")


@router.post("/", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    user_scopes = [user_scope.scope.value for user_scope in user.user_scopes]
    access_token = create_access_token(
        data={"sub": user.email, "scopes": user_scopes},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")