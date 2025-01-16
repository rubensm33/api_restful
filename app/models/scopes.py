from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from config.database import Base
import enum


class ScopeEnum(enum.Enum):
    me = "me"


class UserScopes(Base):
    __tablename__ = "user_scopes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    scope = Column(Enum(ScopeEnum), nullable=False)

    user = relationship("User", back_populates="user_scopes")
