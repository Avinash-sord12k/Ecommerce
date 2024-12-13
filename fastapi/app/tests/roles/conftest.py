from uuid import uuid4

import pytest_asyncio
from httpx import AsyncClient
from loguru import logger
from starlette.status import HTTP_200_OK, HTTP_201_CREATED


@pytest_asyncio.fixture(scope="module")
def role_data():
    """Fixture to provide role data."""
    return {"name": str(uuid4()), "description": str(uuid4())}


@pytest_asyncio.fixture(scope="module")
async def role(client: AsyncClient, role_data: dict, tester_access_token: str):
    logger.info(role_data)
    response = await client.post(
        "/api/v1/role/create",
        json=role_data,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    assert response.status_code == HTTP_201_CREATED
    yield response_json

    response = await client.delete(
        f"/api/v1/role/{response_json['id']}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
