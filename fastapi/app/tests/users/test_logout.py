from uuid import uuid4

import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.users.models import UserRoles


@pytest.mark.asyncio(loop_scope="session")
async def test_user_logout(client: AsyncClient, created_user):
    _, user_data = created_user

    # Login to get token
    login_response = await client.post(
        "/api/v1/users/login",
        data={
            "username": user_data["username"],
            "password": user_data["password"],
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    token = login_response.json()["access_token"]
    client.cookies = {"access_token": token}
    logout_response = await client.get("/api/v1/users/logout")
    client.cookies.clear()

    assert logout_response.status_code == HTTP_200_OK
    assert "access_token" not in logout_response.cookies


@pytest.mark.asyncio(loop_scope="session")
async def test_user_logout_no_token(client: AsyncClient):
    logout_response = await client.get("/api/v1/users/logout")
    assert logout_response.status_code == HTTP_200_OK
    assert "access_token" not in logout_response.cookies


@pytest.mark.asyncio(loop_scope="session")
async def test_user_logout_invalid_token(client: AsyncClient):
    client.cookies = {"access_token": str(uuid4())}
    logout_response = await client.get("/api/v1/users/logout")
    client.cookies.clear()

    assert logout_response.status_code == HTTP_200_OK
    assert "access_token" not in logout_response.cookies
