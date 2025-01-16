from datetime import datetime, timedelta, timezone

import bcrypt
from utils.constants import *
import jwt


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def hash_password(password: str) -> str:

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def check_password(password: str, hashed_password: str) -> bool:

    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
