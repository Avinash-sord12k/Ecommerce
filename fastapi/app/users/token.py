from abc import ABC, abstractmethod
from typing import List, Optional

import jwt
from fastapi import HTTPException, Request
from fastapi.openapi.models import SecurityBase as SecurityBaseModel
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.base import SecurityBase
from loguru import logger
from starlette.status import HTTP_401_UNAUTHORIZED

from app.config import HASHING_ALGORITHM, SECRET_KEY


class TokenExtractorStrategy(ABC):
    @abstractmethod
    async def extract_token(self, request: Request) -> Optional[str]:
        pass

    @abstractmethod
    async def get_user_id(self, token: str) -> Optional[int]:
        pass


class CookieTokenExtractor(TokenExtractorStrategy):
    async def extract_token(self, request: Request) -> Optional[str]:
        try:
            cookie_authorization = request.cookies.get("access_token")
            if not cookie_authorization:
                return None
            return cookie_authorization.replace("Bearer ", "")
        except Exception as e:
            logger.error(f"Error extracting token from cookie: {e}")
            return None

    async def get_user_id(self, token: str) -> Optional[int]:
        try:
            payload = jwt.decode(
                token, SECRET_KEY, algorithms=[HASHING_ALGORITHM]
            )
            return payload.get("user_id")
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        except Exception as e:
            logger.error(f"Error getting user id from token: {e}")
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Authentication failed",
            )


class OAuth2TokenExtractor(TokenExtractorStrategy):
    def __init__(self):
        self.oauth2_scheme = OAuth2PasswordBearer(
            tokenUrl="/api/v1/users/login"
        )

    async def extract_token(self, request: Request) -> Optional[str]:
        try:
            token = await self.oauth2_scheme(request)
            return token
        except HTTPException:
            return None
        except Exception as e:
            logger.error(f"Error extracting OAuth2 token: {e}")
            return None

    async def get_user_id(self, token: str) -> Optional[int]:
        try:
            payload = jwt.decode(
                token, SECRET_KEY, algorithms=[HASHING_ALGORITHM]
            )
            return payload.get("user_id")
        except jwt.ExpiredSignatureError as e:
            logger.error(f"Token expired: {e}")
            return None
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid token: {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting user id from token: {e}")
            return None


class TokenManager:
    def __init__(self, strategies: list[TokenExtractorStrategy]):
        self.strategies = strategies

    async def get_user_id(self, request: Request) -> Optional[int]:
        for strategy in self.strategies:
            if token := await strategy.extract_token(request):
                if user_id := await strategy.get_user_id(token):
                    return user_id

        logger.debug("No token found")
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
