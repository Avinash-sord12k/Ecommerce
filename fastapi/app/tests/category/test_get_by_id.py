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
async def test_get_category_by_id(client: AsyncClient, category_data: dict):
    # Create category
    response = await client.post("/api/v1/category/create", json=category_data)
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_201_CREATED
    assert response_json["name"] == category_data["name"]

    category_id = response_json["id"]

    # Get category by ID
    response = await client.get(f"/api/v1/category/get-by-id/{category_id}")
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == category_id

    # Delete category
    response = await client.delete(f"/api/v1/category/{category_id}")
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == category_id


@pytest.mark.asyncio(loop_scope="session")
async def test_get_nonexistent_category_by_id(client: AsyncClient):
    nonexistent_category_id = 99999  # Assuming 99999 doesn't exist
    response = await client.get(
        f"/api/v1/category/get-by-id/{nonexistent_category_id}"
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_get_category_by_invalid_id(client: AsyncClient):
    invalid_category_id = "invalid_id"
    response = await client.get(
        f"/api/v1/category/get-by-id/{invalid_category_id}"
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_get_category_after_deletion(
    client: AsyncClient, category_data: dict
):
    # Create category
    response = await client.post("/api/v1/category/create", json=category_data)
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_201_CREATED
    assert response_json["name"] == category_data["name"]

    category_id = response_json["id"]

    # Delete the category
    response = await client.delete(f"/api/v1/category/{category_id}")
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == category_id

    # Try to get the deleted category
    response = await client.get(f"/api/v1/category/get-by-id/{category_id}")
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND
