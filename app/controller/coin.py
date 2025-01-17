from datetime import datetime
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.sql import func
from sqlalchemy.orm import Session

from models.coin import Coin
from schemas.coin import CoinAverage, CoinResponse
from services.user_service import get_current_active_user
from schemas.transaction import TransactionResponse, TransactionSell
from models.transaction import Transaction, TransactionTypeEnum
from models.user import User
from config.database import get_db
from repositories.transaction_repository import save_transaction

router = APIRouter(prefix="/coin")


@router.get("/user", response_model=List[CoinResponse], status_code=status.HTTP_200_OK)
def list_user_coins(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    user_coins = db.query(Coin).filter(Coin.user_id == current_user.id).all()
    if not user_coins:
        raise HTTPException(status_code=404, detail="No coins found for the user.")

    return user_coins


@router.get("/average-price", response_model=List[CoinAverage], status_code=status.HTTP_200_OK)
def list_user_coins_average_price(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    user_coins = (
        db.query(
            Coin.user_id,
            Coin.name,
            (func.sum(Coin.price * Coin.quantity) / func.sum(Coin.quantity)).label("average_price"),
            func.sum(Coin.quantity).label("quantity"),
        )
        .filter(Coin.user_id == current_user.id)
        .group_by(Coin.name)
        .all()
    )

    if not user_coins:
        raise HTTPException(status_code=404, detail="No coins found for the user.")

    return [
        CoinAverage(
            user_id=coin.user_id,
            name=coin.name,
            average_price=coin.average_price,
            quantity=coin.quantity,
        )
        for coin in user_coins
    ]


@router.post("/sell", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def sell_coin(
    transaction: TransactionSell,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    coin = db.query(Coin).filter(Coin.user_id == current_user.id, Coin.id == transaction.coin_id).first()
    if not coin:
        raise HTTPException(status_code=404, detail="Coin not found in user portfolio.")

    if coin.quantity < transaction.quantity:
        raise HTTPException(status_code=400, detail="Insufficient quantity of the coin to sell.")

    coin.quantity -= transaction.quantity
    if coin.quantity == 0:
        db.delete(coin)
    else:
        db.add(coin)

    total_value = transaction.quantity * coin.price
    current_user.balance += total_value

    new_transaction = Transaction(
        user_id=current_user.id,
        coin_id=coin.id,
        transaction_type=TransactionTypeEnum.sell,
        transaction_date=datetime.utcnow(),
    )

    save_transaction(db, new_transaction)
    db_user = db.query(User).filter(User.id == current_user.id).first()
    db_user.balance = current_user.balance
    db.commit()
    db.refresh(db_user)

    return TransactionResponse(
        id=new_transaction.id,
        user_id=current_user.id,
        coin_name=coin.name,
        quantity=transaction.quantity,
        total_price=total_value,
        transaction_type=new_transaction.transaction_type.value,
        transaction_date=new_transaction.transaction_date,
    )
