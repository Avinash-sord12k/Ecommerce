import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_category(client: AsyncClient, category_data: dict):
    # Create category
    response = await client.post("/api/v1/category/create", json=category_data)
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_201_CREATED
    assert response_json["name"] == category_data["name"]

    category_id = response_json["id"]

    # Delete category
    response = await client.delete(f"/api/v1/category/{category_id}")
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == category_id


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_nonexistent_category(client: AsyncClient):
    # Try to delete a category that does not exist
    non_existent_category_id = 99999  # Assuming 99999 doesn't exist
    response = await client.delete(
        f"/api/v1/category/{non_existent_category_id}"
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_invalid_category_id(client: AsyncClient):
    # Try to delete a category with an invalid ID (e.g., a string instead of an integer)
    invalid_category_id = "invalid_id"
    response = await client.delete(f"/api/v1/category/{invalid_category_id}")
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_already_deleted_category(
    client: AsyncClient, category_data: dict
):
    # Create category
    response = await client.post("/api/v1/category/create", json=category_data)
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_201_CREATED
    assert response_json["name"] == category_data["name"]

    category_id = response_json["id"]

    # Delete category
    response = await client.delete(f"/api/v1/category/{category_id}")
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == category_id

    # Try deleting the category again
    response = await client.delete(f"/api/v1/category/{category_id}")
    assert response.status_code == HTTP_404_NOT_FOUND
    response_json = response.json()
