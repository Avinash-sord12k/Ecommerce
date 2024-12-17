import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_by_id(
    client: AsyncClient, address: dict, tester_access_token: str
):
    address_id = address["id"]
    response = await client.get(
        f"/api/v1/address/get-by-id/{address_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK


@pytest.mark.asyncio(loop_scope="session")
async def test_get_by_id_invalid_id(
    client: AsyncClient, tester_access_token: str
):
    invalid_address_id = "invalid-id"  # Non-UUID or invalid ID format
    response = await client.get(
        f"/api/v1/address/get-by-id/{invalid_address_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_get_by_id_non_existent_id(
    client: AsyncClient, tester_access_token: str
):
    non_existent_address_id = 99999999  # Non-existent ID
    response = await client.get(
        f"/api/v1/address/get-by-id/{non_existent_address_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_get_by_id_missing_authentication(
    client: AsyncClient, address: dict
):
    address_id = address["id"]
    response = await client.get(
        f"/api/v1/address/get-by-id/{address_id}",
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_401_UNAUTHORIZED
