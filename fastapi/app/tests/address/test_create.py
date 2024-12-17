import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_create_address(
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
async def test_maximum_address_creation_limit(
    client: AsyncClient,
    address: dict,
    create_address_request_payload: dict,
    tester_access_token: str,
):
    address_ids = []
    for _ in range(4):
        response = await client.post(
            "/api/v1/address/create",
            json=create_address_request_payload,
            headers={"Authorization": f"Bearer {tester_access_token}"},
        )
        response_json = response.json()
        logger.debug(response_json)
        assert response.status_code == HTTP_201_CREATED
        address_ids.append(response_json["id"])

    response = await client.post(
        "/api/v1/address/create",
        json=create_address_request_payload,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_400_BAD_REQUEST

    for address_id in address_ids:
        response = await client.delete(
            f"/api/v1/address/{address_id}",
            headers={"Authorization": f"Bearer {tester_access_token}"},
        )
        response_json = response.json()
        logger.debug(response_json)
        assert response.status_code == HTTP_200_OK


@pytest.mark.asyncio(loop_scope="session")
async def test_create_address_without_permissions(
    client: AsyncClient,
    create_address_request_payload: dict,
    admin_access_token: str,
):
    response = await client.post(
        "/api/v1/address/create",
        json=create_address_request_payload,
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.asyncio(loop_scope="session")
async def test_create_address_invalid_payload(
    client: AsyncClient,
    tester_access_token: str,
):
    invalid_payload = {"invalid_field": "invalid_value"}
    response = await client.post(
        "/api/v1/address/create",
        json=invalid_payload,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_create_address_missing_authentication(
    client: AsyncClient,
    create_address_request_payload: dict,
):
    response = await client.post(
        "/api/v1/address/create",
        json=create_address_request_payload,
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_401_UNAUTHORIZED
