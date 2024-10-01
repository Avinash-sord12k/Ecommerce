from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.config import DB_CONFIGS


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = ""
    phone: Optional[str] = ""
    address: Optional[str] = ""


class User(DB_CONFIGS["Base"]):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    username: str = Column(String(255), unique=True, nullable=False)
    email: str = Column(String(255), unique=True, nullable=False)
    password: str = Column(String(255), nullable=False)
    full_name: str = Column(String(255), nullable=True)
    phone: str = Column(String(255), nullable=True)
    address: str = Column(String(255), nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    superuser: bool = Column(Boolean, default=False)
    internal_user: bool = Column(Boolean, default=False)
    date_joined: datetime = Column(DateTime, default=datetime.utcnow)
    last_active: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
