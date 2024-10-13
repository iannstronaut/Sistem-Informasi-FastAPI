from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from services.database import Base
from pydantic import BaseModel, EmailStr

class User(Base):
    __tablename__ = "users"

    id          = Column(Integer, primary_key=True, index=True)
    username    = Column(String(50), unique=True, nullable=False)
    email       = Column(String(100), unique=True, nullable=False)
    password    = Column(String(128), nullable=True)
    createAt    = Column(DateTime, default=datetime.now(timezone.utc))
    updateAt    = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    items = relationship("Item", back_populates="user")

class UserBase(BaseModel):
    username    : str
    email       : EmailStr
    password    : str