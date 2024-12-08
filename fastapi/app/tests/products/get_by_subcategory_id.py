import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_sub_category_id(
    client: AsyncClient, sub_category: tuple, product_data: dict
):
    category_id, subcategory_id = sub_category
    product_data["category_id"] = category_id
    product_data["sub_category_ids"] = [subcategory_id]

    response = await client.post("/api/v1/product/create", json=product_data)
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_201_CREATED
    product_id = response_json["id"]

    response = await client.get(
        f"/api/v1/product/get-by-subcategory-id/{subcategory_id}"
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK
    assert response_json[0]["id"] == product_id

    response = await client.delete(f"/api/v1/product/{product_id}")
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == product_id


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_invalid_sub_category_id(
    client: AsyncClient, sub_category: tuple, product_data: dict
):
    category_id, subcategory_id = sub_category
    product_data["category_id"] = category_id
    product_data["sub_category_ids"] = [subcategory_id]

    response = await client.post("/api/v1/product/create", json=product_data)
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_201_CREATED
    product_id = response_json["id"]

    invalid_subcategory_id = "ABSC"
    response = await client.get(
        f"/api/v1/product/get-by-subcategory-id/{invalid_subcategory_id}"
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    response = await client.delete(f"/api/v1/product/{product_id}")
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == product_id


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_non_existent_sub_category_id(
    client: AsyncClient, sub_category: tuple, product_data: dict
):
    category_id, subcategory_id = sub_category
    product_data["category_id"] = category_id
    product_data["sub_category_ids"] = [subcategory_id]

    response = await client.post("/api/v1/product/create", json=product_data)
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_201_CREATED
    product_id = response_json["id"]

    fake_subcategory_id = (
        9999999  # Assuming this is a non-existent subcategory ID
    )
    response = await client.get(
        f"/api/v1/product/get-by-subcategory-id/{fake_subcategory_id}"
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND

    response = await client.delete(f"/api/v1/product/{product_id}")
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == product_id


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_sub_category_id_without_sub_category_id(
    client: AsyncClient,
):
    response = await client.get("/api/v1/product/get-by-subcategory-id")
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_sub_category_id_without_id(client: AsyncClient):
    response = await client.get("/api/v1/product/get-by-subcategory-id")
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED
