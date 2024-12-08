import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product(client: AsyncClient, sub_category: tuple, product_data: dict):
    category_id, subcategory_id = sub_category
    product_data["category_id"] = category_id
    product_data["sub_category_id"] = subcategory_id

    response = await client.post("/api/v1/product/create", json=product_data)
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_201_CREATED
    assert response_json["name"] == product_data["name"]

    product_id = response_json["id"]
    response = await client.delete(f"/api/v1/product/{product_id}")
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == product_id


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product_without_required_fields(client: AsyncClient, sub_category: tuple):
    category_id, subcategory_id = sub_category
    product_data = {"name": "", "category_id": category_id, "sub_category_id": subcategory_id}
    response = await client.post("/api/v1/product/create", json=product_data)
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product_with_invalid_category_id(client: AsyncClient, sub_category: tuple, product_data: dict):
    _, subcategory_id = sub_category
    product_data["category_id"] = 12345  # Invalid category ID
    product_data["sub_category_id"] = subcategory_id

    response = await client.post("/api/v1/product/create", json=product_data)
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND
