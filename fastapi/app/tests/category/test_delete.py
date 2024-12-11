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
async def test_delete_category(
    client: AsyncClient, category_data: dict, admin_access_token: str
):
    # Create category
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

    # Delete category
    response = await client.delete(
        f"/api/v1/category/{category_id}",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == category_id


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_category_without_enough_permissions(
    client: AsyncClient,
    category_data: dict,
    customer_access_token: str,
    seller_access_token: str,
):
    # Create category using customer account
    response = await client.post(
        "/api/v1/category/create",
        json=category_data,
        headers={"Authorization": f"Bearer {customer_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_403_FORBIDDEN

    # Create category using seller account
    response = await client.post(
        "/api/v1/category/create",
        json=category_data,
        headers={"Authorization": f"Bearer {seller_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_nonexistent_category(
    client: AsyncClient, admin_access_token: str
):
    # Try to delete a category that does not exist
    non_existent_category_id = 99999  # Assuming 99999 doesn't exist
    response = await client.delete(
        f"/api/v1/category/{non_existent_category_id}",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_invalid_category_id(
    client: AsyncClient, admin_access_token: str
):
    # Try to delete a category with an invalid ID (e.g., a string instead of an integer)
    invalid_category_id = "invalid_id"
    response = await client.delete(
        f"/api/v1/category/{invalid_category_id}",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
