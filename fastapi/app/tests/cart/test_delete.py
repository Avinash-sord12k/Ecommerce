import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
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
        "/api/v1/cart",
        params={"id": cart_id},
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_someone_elses_cart(
    client: AsyncClient,
    cart: dict,
    customer_access_token: str,
):
    response = await client.delete(
        "/api/v1/cart",
        params={"id": cart["id"]},
        headers={"Authorization": f"Bearer {customer_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


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
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_cart_with_invalid_id(
    client: AsyncClient, tester_access_token: str
):
    response = await client.delete(
        "/api/v1/cart",
        params={"id": "invalid_id"},
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
