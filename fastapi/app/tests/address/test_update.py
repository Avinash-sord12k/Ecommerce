from uuid import uuid4

import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_update_address(
    client: AsyncClient,
    address: dict,
    create_address_request_payload: dict,
    tester_access_token: str,
):
    request_payload = create_address_request_payload.copy()
    request_payload["name"] = str(uuid4())
    request_payload["address"] = str(uuid4())

    address_id = address["id"]
    response = await client.put(
        f"/api/v1/address/update/{address_id}",
        json=request_payload,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)

    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == address_id
    assert response_json["name"] == request_payload["name"]
    assert response_json["address"] == request_payload["address"]


@pytest.mark.asyncio(loop_scope="session")
async def test_update_address_with_invalid_id(
    client: AsyncClient,
    create_address_request_payload: dict,
    tester_access_token: str,
):
    invalid_address_id = "invalid-id"  # Non-UUID format
    request_payload = create_address_request_payload.copy()
    request_payload["name"] = str(uuid4())
    request_payload["address"] = str(uuid4())

    response = await client.put(
        f"/api/v1/address/update/{invalid_address_id}",
        json=request_payload,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)

    assert (
        response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    )  # Expect a validation error


@pytest.mark.asyncio(loop_scope="session")
async def test_update_address_with_non_existent_id(
    client: AsyncClient,
    create_address_request_payload: dict,
    tester_access_token: str,
):
    non_existent_address_id = 999999999
    request_payload = create_address_request_payload.copy()
    request_payload["name"] = str(uuid4())
    request_payload["pincode"] = str(uuid4())

    response = await client.put(
        f"/api/v1/address/update/{non_existent_address_id}",
        json=request_payload,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)

    assert response.status_code == HTTP_404_NOT_FOUND  # Address not found


@pytest.mark.asyncio(loop_scope="session")
async def test_update_address_with_empty_payload(
    client: AsyncClient, address: dict, tester_access_token: str
):
    address_id = address["id"]
    empty_payload = {}

    response = await client.put(
        f"/api/v1/address/update/{address_id}",
        json=empty_payload,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)

    assert (
        response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    )  # Missing required fields


@pytest.mark.asyncio(loop_scope="session")
async def test_update_address_with_invalid_data_types(
    client: AsyncClient, address: dict, tester_access_token: str
):
    address_id = address["id"]
    invalid_payload = {"name": 12345, "address": None}  # Invalid data types

    response = await client.put(
        f"/api/v1/address/update/{address_id}",
        json=invalid_payload,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)

    assert (
        response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    )  # Validation error


@pytest.mark.asyncio(loop_scope="session")
async def test_update_address_simulate_internal_server_error(
    client: AsyncClient, address: dict, tester_access_token: str, monkeypatch
):
    address_id = address["id"]
    valid_payload = {"name": str(uuid4()), "address": str(uuid4())}

    # Simulate server error by mocking the response
    async def mock_put(*args, **kwargs):
        class MockResponse:
            status_code = HTTP_500_INTERNAL_SERVER_ERROR

            async def json(self):
                return {"detail": "Internal Server Error"}

        return MockResponse()

    monkeypatch.setattr(client, "put", mock_put)

    response = await client.put(
        f"/api/v1/address/update/{address_id}",
        json=valid_payload,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = await response.json()
    logger.debug(response_json)

    assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR
