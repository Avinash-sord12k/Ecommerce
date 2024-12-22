import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_update_cart(
    client: AsyncClient,
    cart: dict,
    create_cart_request_payload: dict,
    tester_access_token: str,
):
    cart_id = cart["id"]
    request_payload = create_cart_request_payload.copy()
    request_payload["name"] = "new name"

    response = await client.put(
        f"/api/v1/cart/update/{cart_id}",
        json=request_payload,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == cart["id"]


@pytest.mark.asyncio(loop_scope="session")
async def test_update_someone_else_cart(
    client: AsyncClient,
    cart: dict,
    create_cart_request_payload: dict,
    customer_access_token: str,
):
    cart_id = cart["id"]
    request_payload = create_cart_request_payload.copy()
    request_payload["name"] = "new name"
    logger.debug(request_payload)

    response = await client.put(
        f"/api/v1/cart/update/{cart_id}",
        json=request_payload,
        headers={"Authorization": f"Bearer {customer_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_update_cart_without_id(
    client: AsyncClient,
    create_cart_request_payload: dict,
    tester_access_token: str,
):
    response = await client.put(
        "/api/v1/cart/update",
        json=create_cart_request_payload,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_update_cart_with_invalid_id(
    client: AsyncClient,
    create_cart_request_payload: dict,
    tester_access_token: str,
):
    response = await client.put(
        "/api/v1/cart/update/invalid-id",
        json=create_cart_request_payload,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
