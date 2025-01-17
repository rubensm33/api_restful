from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from config.database import Base


class Coin(Base):
    __tablename__ = "coins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    price = Column(Float)
    quantity = Column(Integer, nullable=False)
    volume_24h = Column(Float)
    percent_change_1h = Column(Float)
    percent_change_24h = Column(Float)
    percent_change_7d = Column(Float)
    
    user = relationship("User", back_populates="coins")

    @declared_attr
    def type(cls):
        return Column(String(50))
