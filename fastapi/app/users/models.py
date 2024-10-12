from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from typing_extensions import Optional

from app.config import Base


class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRead(BaseModel):
    id: int
    username: str
    email: Optional[str]
    full_name: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    is_internal_user: bool
    date_joined: datetime
    last_active: datetime

    class Config:
        from_attributes = True


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    username: str = Column(String(255), unique=True, nullable=False)
    password: str = Column(String(255), nullable=False)
    email: str = Column(String(255), unique=True, nullable=True)
    full_name: str = Column(String(255), nullable=True)
    phone: str = Column(String(255), nullable=True)
    address: str = Column(String(255), nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    is_internal_user: bool = Column(Boolean, default=False)
    date_joined: datetime = Column(DateTime, default=datetime.utcnow)
    last_active: datetime = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
