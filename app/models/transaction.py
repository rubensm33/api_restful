from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, Enum
from sqlalchemy.orm import relationship
from config.database import Base
import enum


class TransactionTypeEnum(enum.Enum):
    sell = "sell"
    buy = "buy"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    coin_id = Column(Integer, ForeignKey("coins.id"), nullable=False)
    transaction_date = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    transaction_type = Column(Enum(TransactionTypeEnum), nullable=False)

    coin = relationship("Coin")
    user = relationship("User", back_populates="transactions")
