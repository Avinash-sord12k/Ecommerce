from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from loguru import logger
from starlette.status import HTTP_401_UNAUTHORIZED

from app.config import HASHING_ALGORITHM, SECRET_KEY
from app.users.auth import (
    AuthenticationContext,
    CookieAuthStrategy,
    OAuth2AuthStrategy,
)
from app.users.token import (
    CookieTokenExtractor,
    OAuth2TokenExtractor,
    TokenExtractorStrategy,
    TokenManager,
)

cookie_strategy = CookieAuthStrategy()
oauth2_strategy = OAuth2AuthStrategy()
auth_context = AuthenticationContext([cookie_strategy, oauth2_strategy])
token_manager = TokenManager([CookieTokenExtractor(), OAuth2TokenExtractor()])


def hash_password(password):
    hash_bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hash_bytes.decode("utf-8")


def verify_password(password: str, hash: str):
    return bcrypt.checkpw(password.encode("utf-8"), hash.encode("utf-8"))


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expires_delta = expires_delta or timedelta(minutes=15)
    to_encode.update({"exp": datetime.now(timezone.utc) + expires_delta})
    encoded_jwt = jwt.encode(
        payload=to_encode, key=SECRET_KEY, algorithm=HASHING_ALGORITHM
    )
    return encoded_jwt


async def token_exists(request: Request) -> bool:
    return await auth_context.authenticate(request)


async def get_current_user_id(request: Request) -> int:
    return await token_manager.get_user_id(request)
