from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from services.database import Base
from pydantic import BaseModel, EmailStr

class User(Base):
    __tablename__ = "users"

    id          = Column(Integer, primary_key=True, index=True)
    username    = Column(String(50), unique=True, nullable=False)
    email       = Column(String(100), unique=True, nullable=False)
    fullname    = Column(String(50), nullable=False)
    password    = Column(String(128), nullable=True)
    is_active   = Column(Boolean, default=False)
    createAt    = Column(DateTime, default=datetime.now(timezone.utc))
    updateAt    = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


class UserBase(BaseModel):
    username    : str
    fullname    : str
    email       : EmailStr
    password    : str


class UserLogin(BaseModel):
    username: str
    password: str