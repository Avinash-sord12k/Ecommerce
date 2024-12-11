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
    client: AsyncClient, product: dict, seller_access_token: str
):
    subcategory_id = product["sub_category_ids"][0]
    response = await client.get(
        f"/api/v1/product/get-by-subcategory-id/{subcategory_id}",
        headers={"Authorization": f"Bearer {seller_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_invalid_sub_category_id(
    client: AsyncClient, product: dict, seller_access_token: str
):
    invalid_subcategory_id = "ABSC"
    response = await client.get(
        f"/api/v1/product/get-by-subcategory-id/{invalid_subcategory_id}",
        headers={"Authorization": f"Bearer {seller_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_non_existent_sub_category_id(
    client: AsyncClient, product: dict, seller_access_token: str
):
    fake_subcategory_id = 9999999
    response = await client.get(
        f"/api/v1/product/get-by-subcategory-id/{fake_subcategory_id}",
        headers={"Authorization": f"Bearer {seller_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


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
