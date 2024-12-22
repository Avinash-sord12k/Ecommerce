import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_carts(
    client: AsyncClient, cart: dict, tester_access_token: str
):
    response = await client.get(
        "/api/v1/cart/get-all",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.info(response_json)
    assert response.status_code == HTTP_200_OK

    # Verify pagination fields exist
    assert "items" in response_json
    assert "total" in response_json
    assert "page" in response_json
    assert "page_size" in response_json
    assert "total_pages" in response_json
    assert "has_next" in response_json
    assert "has_previous" in response_json

    cart_id = cart["id"]
    all_carts = [c for c in response_json["items"] if c["id"] == cart_id]
    assert len(all_carts) == 1

    # Verify cart structure
    found_cart = all_carts[0]
    assert "name" in found_cart
    assert "status" in found_cart
    assert "items" in found_cart


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_carts_with_pagination(
    client: AsyncClient, cart: dict, tester_access_token: str
):
    response = await client.get(
        "/api/v1/cart/get-all?page=1&page_size=5",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.info(response_json)
    assert response.status_code == HTTP_200_OK
    assert response_json["page"] == 1
    assert response_json["page_size"] == 5


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_carts_invalid_page(
    client: AsyncClient, tester_access_token: str
):
    response = await client.get(
        "/api/v1/cart/get-all?page=0",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_carts_without_permission(
    client: AsyncClient, cart: dict, seller_access_token: str
):
    response = await client.get(
        "/api/v1/cart/get-all",
        headers={"Authorization": f"Bearer {seller_access_token}"},
    )
    response_json = response.json()
    logger.info(response_json)
    assert response.status_code == HTTP_403_FORBIDDEN
