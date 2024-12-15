import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_cart(
    client: AsyncClient,
    create_cart_request_payload: dict,
    tester_access_token: str,
):
    response = await client.post(
        "/api/v1/cart/create",
        json=create_cart_request_payload,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_201_CREATED

    cart_id = response_json["id"]
    response = await client.delete(
        f"/api/v1/cart/{cart_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_cart_without_permissions(
    client: AsyncClient,
    create_cart_request_payload: dict,
    admin_access_token: str,
    seller_access_token: str,
):
    response = await client.post(
        "/api/v1/cart/create",
        json=create_cart_request_payload,
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_403_FORBIDDEN

    response = await client.post(
        "/api/v1/cart/create",
        json=create_cart_request_payload,
        headers={"Authorization": f"Bearer {seller_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_cart_without_id(
    client: AsyncClient, tester_access_token: str
):
    response = await client.delete(
        "/api/v1/cart",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_cart_with_invalid_id(
    client: AsyncClient, tester_access_token: str
):
    response = await client.delete(
        "/api/v1/cart/invalid_id",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
