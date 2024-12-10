import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_create_sub_category(
    client: AsyncClient, category: str, sub_category_data: dict
):
    # Create subcategory
    sub_category_data["category_id"] = category
    response = await client.post(
        "/api/v1/subcategory/create", json=sub_category_data
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_201_CREATED
    assert response_json["name"] == sub_category_data["name"]

    subcategory_id = response_json["id"]

    # Delete subcategory
    response = await client.delete(f"/api/v1/subcategory/{subcategory_id}")
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == subcategory_id


@pytest.mark.asyncio(loop_scope="session")
async def test_create_sub_category_with_nonexistent_category(
    client: AsyncClient, sub_category_data: dict
):
    nonexistent_category_id = 99999  # Assuming 99999 doesn't exist
    sub_category_data["category_id"] = nonexistent_category_id
    response = await client.post(
        "/api/v1/subcategory/create", json=sub_category_data
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_create_sub_category_with_invalid_category_id(
    client: AsyncClient, sub_category_data: dict
):
    invalid_category_id = "invalid_id"
    sub_category_data["category_id"] = invalid_category_id
    response = await client.post(
        "/api/v1/subcategory/create", json=sub_category_data
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_create_sub_category_without_required_fields(
    client: AsyncClient, category: str
):
    # Try to create subcategory without a name (missing required field)
    sub_category_data = {"category_id": category}  # Missing 'name' field
    response = await client.post(
        "/api/v1/subcategory/create", json=sub_category_data
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_create_sub_category_with_duplicate_name(
    client: AsyncClient,
    category: str,
    sub_category_data: dict,
):
    # Create the first subcategory
    sub_category_data["category_id"] = category
    response = await client.post(
        "/api/v1/subcategory/create", json=sub_category_data
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_201_CREATED
    assert response_json["name"] == sub_category_data["name"]

    # Try to create a subcategory with the same name under the same category
    subcategory_id = response_json["id"]
    sub_category_data["name"] = sub_category_data["name"]  # Same name
    response = await client.post(
        "/api/v1/subcategory/create", json=sub_category_data
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_400_BAD_REQUEST

    # delete subcategory
    response = await client.delete(f"/api/v1/subcategory/{subcategory_id}")
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == subcategory_id
