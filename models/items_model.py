from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from services.database import Base
from pydantic import BaseModel

class Item(Base):
    __tablename__ = "items"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(50), nullable=False)
    content     = Column(String(100), nullable=False)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    createAt    = Column(DateTime, default=datetime.now(timezone.utc))
    updateAt    = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    user_id     = Column(Integer, ForeignKey("users.id"))

class ItemBase(BaseModel):
    title       : str
    content     : str
