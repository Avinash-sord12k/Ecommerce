from uuid import uuid4

import pytest_asyncio
from httpx import AsyncClient
from loguru import logger
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.address.models import AddressCreateModel


@pytest_asyncio.fixture(scope="session")
def create_address_request_payload():
    return AddressCreateModel(
        name=str(uuid4()),
        address=str(uuid4()),
        city=str(uuid4()),
        state=str(uuid4()),
        country=str(uuid4()),
        pincode=str(uuid4()),
    ).model_dump()


@pytest_asyncio.fixture(scope="session")
async def address(
    client: AsyncClient,
    create_address_request_payload: dict,
    tester_access_token: str,
):
    response = await client.post(
        "/api/v1/address/create",
        json=create_address_request_payload,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_201_CREATED
    yield response_json

    address_id = response_json["id"]
    response = await client.delete(
        f"/api/v1/address/{address_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK
