import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_create_role(client: AsyncClient, role_data: dict):
    response = await client.post("/api/v1/role/create", json=role_data)
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_201_CREATED


@pytest.mark.asyncio(loop_scope="session")
async def test_create_role_with_existing_name(
    client: AsyncClient, role_data: dict
):
    response = await client.post("/api/v1/role/create", json=role_data)
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.asyncio(loop_scope="session")
async def test_create_role_with_invalid_name(
    client: AsyncClient, role_data: dict
):
    role_data["name"] = ""
    response = await client.post("/api/v1/role/create", json=role_data)
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
