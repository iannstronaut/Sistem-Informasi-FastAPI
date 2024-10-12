from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id          = Column(Integer, primary_key=True, index=True)
    username    = Column(String(50), unique=True, nullable=False)
    email       = Column(String(100), unique=True, nullable=False)
    password    = Column(String(128), nullable=True)
    createAt    = Column(DateTime, default=datetime.now(timezone.utc))
    updateAt    = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

class Item(Base):
    __tablename__ = "items"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(50), nullable=False)
    content     = Column(String(100), nullable=False)
    user_id     = Column(Integer, nullable=False)
    createAt    = Column(DateTime, default=datetime.now(timezone.utc))
    updateAt    = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
