from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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
