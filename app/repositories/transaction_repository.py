from sqlalchemy.orm import Session
from models.transaction import Transaction


def save_transaction(db: Session, transaction: Transaction):
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction
