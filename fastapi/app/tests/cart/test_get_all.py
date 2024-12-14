import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import HTTP_200_OK, HTTP_403_FORBIDDEN


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

    cart_id = cart["id"]
    all_carts = [c for c in response_json["carts"] if c["id"] == cart_id]
    assert len(all_carts) == 1


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
