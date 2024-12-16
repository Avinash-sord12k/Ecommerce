import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_create_cart(
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
async def test_create_with_invalid_name(
    client: AsyncClient, tester_access_token: str
):
    response = await client.post(
        "/api/v1/cart/create",
        json={"name": ""},
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_create_with_reminder_date_less_than_now(
    client: AsyncClient, tester_access_token: str
):
    response = await client.post(
        "/api/v1/cart/create",
        json={"name": "test", "reminder_date": "2023-01-01"},
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_create_with_invalid_reminder_date(
    client: AsyncClient,
    tester_access_token: str,
):
    response = await client.post(
        "/api/v1/cart/create",
        json={"name": "test", "reminder_date": "invalid_date"},
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_create_cart_without_permissions(
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
