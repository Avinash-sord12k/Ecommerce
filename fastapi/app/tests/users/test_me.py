from uuid import uuid4

import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.users.models import UserRoles


@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_profile(client: AsyncClient, created_user):
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

    profile_response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert profile_response.status_code == HTTP_200_OK
    user_profile = profile_response.json()

    assert user_profile["username"] == user_data["username"]
    assert user_profile["email"] == user_data["email"]


@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_profile_by_access_token(
    client: AsyncClient, created_user
):
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
    profile_response = await client.get("/api/v1/users/me")
    client.cookies.clear()

    assert profile_response.status_code == HTTP_200_OK

    user_profile = profile_response.json()
    assert user_profile["username"] == user_data["username"]
    assert user_profile["email"] == user_data["email"]

    client.cookies.clear()
