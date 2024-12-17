from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserRoles(Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    SELLER = "seller"
    TESTER = "tester"


class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: UserRoles = UserRoles.CUSTOMER


class UserLogin(BaseModel):
    username: str
    password: str


class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRead(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role_id: int
    is_internal_user: bool
    date_joined: datetime
    last_active: datetime
    model_config = ConfigDict(from_attributes=True)
