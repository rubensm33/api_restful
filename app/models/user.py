from sqlalchemy import Boolean, Column, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    balance = Column(Float)

    user_scopes = relationship("UserScopes", back_populates="user")
    coins = relationship("Coin", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")

    @declared_attr
    def type(cls):
        return Column(String(50))
