import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_create_category(
    client: AsyncClient, category_data: dict, admin_access_token: str
):
    response = await client.post(
        "/api/v1/category/create",
        json=category_data,
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_201_CREATED
    assert response_json["name"] == category_data["name"]

    category_id = response_json["id"]
    response = await client.delete(
        f"/api/v1/category/{category_id}",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == category_id


@pytest.mark.asyncio(loop_scope="session")
async def test_create_category_without_enough_permissions(
    client: AsyncClient,
    category_data: dict,
    customer_access_token: str,
    seller_access_token: str,
):
    response = await client.post(
        "/api/v1/category/create",
        json=category_data,
        headers={"Authorization": f"Bearer {customer_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_403_FORBIDDEN

    response = await client.post(
        "/api/v1/category/create",
        json=category_data,
        headers={"Authorization": f"Bearer {seller_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.asyncio(loop_scope="session")
async def test_create_category_missing_name(
    client: AsyncClient, admin_access_token: str
):
    category_data = {"name": ""}
    response = await client.post(
        "/api/v1/category/create",
        json=category_data,
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_create_category_invalid_data(
    client: AsyncClient, admin_access_token: str
):
    category_data = {"name": 12345}  # Invalid data type for name
    response = await client.post(
        "/api/v1/category/create",
        json=category_data,
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
