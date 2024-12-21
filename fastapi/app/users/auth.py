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


class CookieAuthentication(SecurityBase):
    def __init__(
        self,
        *,
        cookie_name: str = "access_token",
        scheme_name: str = "Cookie",
        description: str = "Cookie authentication",
        auto_error: bool = True,
    ):
        self.cookie_name = cookie_name
        self.scheme_name = scheme_name
        self.description = description
        self.auto_error = auto_error
        self.model = SecurityBaseModel(
            type="apiKey", in_="cookie", name=cookie_name
        )

    async def __call__(self, request: Request) -> Optional[str]:
        cookie_authorization = request.cookies.get(self.cookie_name)

        if not cookie_authorization and self.auto_error:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated"
            )
        return cookie_authorization


class AuthenticationStrategy(ABC):
    @abstractmethod
    async def authenticate(self, request: Request) -> Optional[str]:
        pass

    @abstractmethod
    def get_security_scheme(self) -> SecurityBase:
        pass


class CookieAuthStrategy(AuthenticationStrategy):
    def __init__(
        self,
        cookie_name: str = "access_token",
        scheme_name: str = "Cookie",
        description: str = "Cookie authentication",
        auto_error: bool = True,
    ):
        self.cookie_name = cookie_name
        self.scheme_name = scheme_name
        self.description = description
        self.auto_error = auto_error
        self._security_scheme = CookieAuthentication(
            cookie_name=cookie_name,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def authenticate(self, request: Request) -> Optional[str]:
        return await self._security_scheme(request)

    def get_security_scheme(self) -> SecurityBase:
        return self._security_scheme


class OAuth2AuthStrategy(AuthenticationStrategy):
    def __init__(
        self, token_url: str = "/api/v1/users/login", auto_error: bool = True
    ):
        self.token_url = token_url
        self.auto_error = auto_error
        self._security_scheme = OAuth2PasswordBearer(
            tokenUrl=token_url, auto_error=auto_error
        )

    async def authenticate(self, request: Request) -> Optional[str]:
        return await self._security_scheme(request)

    def get_security_scheme(self) -> SecurityBase:
        return self._security_scheme


class AuthenticationContext:
    def __init__(self, strategies: List[AuthenticationStrategy]):
        self.strategies = strategies
        if not self.strategies:
            raise ValueError(
                "Authentication context must have at least one strategy"
            )

    async def authenticate(self, request: Request) -> Optional[str]:
        for strategy in self.strategies:
            try:
                if token := await strategy.authenticate(request):
                    logger.debug(f"login with {strategy=}")
                    return token
            except HTTPException:
                continue

        logger.debug("No token found")
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    def get_security_schemes(self) -> List[SecurityBase]:
        return [strategy.get_security_scheme() for strategy in self.strategies]
