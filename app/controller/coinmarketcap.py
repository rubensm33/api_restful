from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
import time

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
from schemas.coin import CoinInfo
from services.coin_service import get_coin_data_from_broker_api

router = APIRouter(prefix="/actives")


@router.post("")
async def actives(coin_name: dict):
    coin_name = coin_name.popitem()[1]

    coin_info = get_coin_data_from_broker_api(coin_name)

    return coin_info
