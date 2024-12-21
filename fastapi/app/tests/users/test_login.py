from uuid import uuid4

import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.users.models import UserRoles


@pytest.mark.asyncio(loop_scope="session")
async def test_user_login(client: AsyncClient, created_user):
    _, user_data = created_user
    login_response = await client.post(
        "/api/v1/users/login",
        data={
            "username": user_data["username"],
            "password": user_data["password"],
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_response.status_code == HTTP_200_OK
    assert "access_token" in login_response.json()


@pytest.mark.asyncio(loop_scope="session")
async def test_user_login_token_cookie(client: AsyncClient, created_user):
    _, user_data = created_user
    login_response = await client.post(
        "/api/v1/users/login",
        data={
            "username": user_data["username"],
            "password": user_data["password"],
        },
        params={"set_cookie": "true"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_response.status_code == HTTP_200_OK
    assert "access_token" in login_response.cookies
