from uuid import uuid4

import pytest_asyncio
from httpx import AsyncClient
from loguru import logger
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.users.models import UserRoles


@pytest_asyncio.fixture(loop_scope="session")
async def test_user_data():
    return {
        "username": str(uuid4()),
        "password": str(uuid4()),
        "email": str(uuid4()),
        "full_name": str(uuid4()),
        "phone": str(uuid4()),
        "role": UserRoles.CUSTOMER.value,
    }


@pytest_asyncio.fixture(loop_scope="session")
async def created_user(client: AsyncClient, test_user_data):
    create_response = await client.post(
        "/api/v1/users/register", json=test_user_data
    )
    assert create_response.status_code == HTTP_201_CREATED
    yield create_response.json(), test_user_data

    logger.debug("Teardown: Deleting user")
