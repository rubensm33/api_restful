from datetime import datetime
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models.coin import Coin
from services.user_service import get_current_active_user
from schemas.transaction import TransactionCreate, TransactionResponse
from models.transaction import Transaction, TransactionTypeEnum
from models.user import User
from config.database import get_db
from services.coin_service import get_coin_data_from_broker_api
from repositories.transaction_repository import save_transaction
from repositories.coin_repository import save_coin

router = APIRouter(prefix="/transactions")


@router.post("/buy", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def buy_coin(
    transaction: TransactionCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    coin_data = get_coin_data_from_broker_api(transaction.coin_name)

    if not coin_data:
        raise HTTPException(status_code=404, detail="Coin not found in external API")

    total_price = transaction.quantity * coin_data.price
    if current_user.balance < total_price:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    current_user.balance -= total_price

    coin = save_coin(db, coin_data, current_user.id, transaction.quantity)

    new_transaction = Transaction(
        user_id=current_user.id,
        coin_id=coin.id,
        coin_name=coin.name,
        quantity=transaction.quantity,
        total_price=total_price,
        transaction_type=TransactionTypeEnum.buy,
        transaction_date=datetime.now(),
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
        quantity=coin.quantity,
        total_price=coin.price,
        transaction_type=new_transaction.transaction_type.value,
        transaction_date=new_transaction.transaction_date,
    )


@router.get("", response_model=List[TransactionResponse], status_code=status.HTTP_200_OK)
def list_user_transactions(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):

    user_transactions = db.query(Transaction).filter(Transaction.user_id == current_user.id).all()
    if not user_transactions:
        raise HTTPException(status_code=404, detail="No transactions found for the user.")

    return [
        TransactionResponse(
            id=transaction.id,
            user_id=transaction.user_id,
            coin_name=transaction.coin_name,
            quantity=transaction.quantity,
            total_price=transaction.total_price,
            transaction_type=transaction.transaction_type.value,
            transaction_date=transaction.transaction_date,
        )
        for transaction in user_transactions
    ]
