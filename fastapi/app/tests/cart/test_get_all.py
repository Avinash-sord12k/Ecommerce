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
async def test_get_cart_by_id(
    client: AsyncClient, cart: dict, tester_access_token: str
):
    cart_id = cart["id"]
    response = await client.get(
        f"/api/v1/cart/get-all?cart_id={cart_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.info(response_json)

    assert response.status_code == HTTP_200_OK
    assert len(response_json["items"]) == 1
    assert response_json["items"][0]["id"] == cart_id
    assert response_json["total"] == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_get_cart_with_items(
    client: AsyncClient, cart: dict, cart_item: dict, tester_access_token: str
):
    cart_id = cart["id"]
    response = await client.get(
        f"/api/v1/cart/get-all?cart_id={cart_id}&get_items=true",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.info(response_json)

    assert response.status_code == HTTP_200_OK
    assert len(response_json["items"]) == 1

    found_cart = response_json["items"][0]
    assert "items" in found_cart
    assert len(found_cart["items"]) > 0

    cart_item = found_cart["items"][0]
    assert "product_id" in cart_item
    assert "quantity" in cart_item
    assert "cart_id" in cart_item
    assert cart_item["cart_id"] == cart_id


@pytest.mark.asyncio(loop_scope="session")
async def test_get_cart_without_items(
    client: AsyncClient, cart: dict, cart_item: dict, tester_access_token: str
):
    cart_id = cart["id"]
    response = await client.get(
        f"/api/v1/cart/get-all?cart_id={cart_id}&get_items=false",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.info(response_json)

    assert response.status_code == HTTP_200_OK
    assert len(response_json["items"]) == 1

    found_cart = response_json["items"][0]
    assert "items" in found_cart
    assert len(found_cart["items"]) == 0


@pytest.mark.asyncio(loop_scope="session")
async def test_get_nonexistent_cart_id(
    client: AsyncClient, tester_access_token: str
):
    response = await client.get(
        "/api/v1/cart/get-all?cart_id=99999",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.info(response_json)

    assert response.status_code == HTTP_200_OK
    assert len(response_json["items"]) == 0
    assert response_json["total"] == 1


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
