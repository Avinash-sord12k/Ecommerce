import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_add_items_to_cart(
    client: AsyncClient,
    cart: dict,
    product: dict,
    add_to_cart_request_payload: dict,
    tester_access_token: str,
):
    product_id = product["id"]
    request_payload = add_to_cart_request_payload.copy()

    request_payload["cart_id"] = cart["id"]
    request_payload["product_id"] = product_id
    request_payload["quantity"] = 1

    response = await client.post(
        "/api/v1/cart/add-item",
        json=request_payload,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK

    cart_id = cart["id"]
    response = await client.delete(
        f"/api/v1/cart/remove-item/{cart_id}/{product_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK


@pytest.mark.asyncio(loop_scope="session")
async def test_add_items_to_someone_else_cart(
    client: AsyncClient,
    cart: dict,
    product: dict,
    add_to_cart_request_payload: dict,
    customer_access_token: str,
):
    product_id = product["id"]
    request_payload = add_to_cart_request_payload.copy()

    request_payload["cart_id"] = cart["id"]
    request_payload["product_id"] = product_id
    request_payload["quantity"] = 1

    response = await client.post(
        "/api/v1/cart/add-item",
        json=request_payload,
        headers={"Authorization": f"Bearer {customer_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_add_items_to_cart_without_id(
    client: AsyncClient,
    add_to_cart_request_payload: dict,
    tester_access_token: str,
):
    request_payload = add_to_cart_request_payload.copy()
    request_payload["cart_id"] = None

    response = await client.post(
        "/api/v1/cart/add-item",
        json=request_payload,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
