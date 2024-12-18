import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_address(
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

    address_id = response_json["id"]
    response = await client.delete(
        f"/api/v1/address/{address_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_someone_elses_address(
    client: AsyncClient, address: dict, customer_access_token: str
):
    address_id = address["id"]
    response = await client.delete(
        f"/api/v1/address/{address_id}",
        headers={"Authorization": f"Bearer {customer_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_non_existent_address(
    client: AsyncClient, tester_access_token: str
):
    non_existent_address_id = 99999999  # Non-existent ID
    response = await client.delete(
        f"/api/v1/address/{non_existent_address_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_address_without_permission(
    client: AsyncClient, admin_access_token: str
):
    response = await client.delete(
        "/api/v1/address/1",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_403_FORBIDDEN
