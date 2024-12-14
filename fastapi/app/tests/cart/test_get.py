import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_a_cart(
    client: AsyncClient, cart: dict, tester_access_token: str
):
    cart_id = cart["id"]
    response = await client.get(
        f"/api/v1/cart/{cart_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    logger.info(response.json())
    assert response.status_code == HTTP_200_OK


@pytest.mark.asyncio(loop_scope="session")
async def test_get_a_cart_without_id(
    client: AsyncClient, tester_access_token: str
):
    response = await client.get(
        "/api/v1/cart",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    logger.info(response.json())
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_get_a_cart_with_invalid_id(
    client: AsyncClient, cart: dict, tester_access_token: str
):
    invalid_cart_id = "invalid_id"
    response = await client.get(
        f"/api/v1/cart/{invalid_cart_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    logger.info(response.json())
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
