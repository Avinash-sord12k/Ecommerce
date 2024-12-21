from uuid import uuid4

import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.users.models import UserRoles


@pytest.mark.asyncio(loop_scope="session")
async def test_user_registration(client: AsyncClient, test_user_data):
    create_response = await client.post(
        "/api/v1/users/register", json=test_user_data
    )
    assert create_response.status_code == HTTP_201_CREATED

    created_user = create_response.json()
    assert created_user["username"] == test_user_data["username"]


@pytest.mark.asyncio(loop_scope="session")
async def test_user_registration_missing_fields(client: AsyncClient):
    incomplete_data = {"username": "testuser"}

    response = await client.post(
        "/api/v1/users/register", json=incomplete_data
    )
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_user_registration_duplicate_username(
    client: AsyncClient, test_user_data
):
    await client.post("/api/v1/users/register", json=test_user_data)

    duplicate_data = test_user_data.copy()
    duplicate_data["email"] = "another@email.com"

    response = await client.post("/api/v1/users/register", json=duplicate_data)
    assert response.status_code == HTTP_409_CONFLICT
