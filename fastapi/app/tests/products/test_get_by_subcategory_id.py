import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_sub_category_id(
    client: AsyncClient, product: dict, seller_access_token: str
):
    subcategory_id = product["sub_category_ids"][0]
    page = 1
    page_size = 10

    response = await client.get(
        "/api/v1/product/get-by-subcategory-id",
        params={
            "sub_category_id": subcategory_id,
            "page": page,
            "page_size": page_size,
        },
        headers={"Authorization": f"Bearer {seller_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)

    assert response.status_code == HTTP_200_OK
    assert "items" in response_json
    assert "total" in response_json
    assert "page" in response_json
    assert "page_size" in response_json
    assert "total_pages" in response_json
    assert response_json["page"] == page
    assert response_json["page_size"] == page_size


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_invalid_sub_category_id(
    client: AsyncClient, product: dict, seller_access_token: str
):
    invalid_subcategory_id = "ABSC"
    page = 1
    page_size = 10
    response = await client.get(
        "/api/v1/product/get-by-subcategory-id",
        params={
            "sub_category_id": invalid_subcategory_id,
            "page": page,
            "page_size": page_size,
        },
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
    page = 1
    page_size = 10
    response = await client.get(
        "/api/v1/product/get-by-subcategory-id",
        params={
            "sub_category_id": fake_subcategory_id,
            "page": page,
            "page_size": page_size,
        },
        headers={"Authorization": f"Bearer {seller_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_sub_category_id_without_sub_category_id(
    client: AsyncClient, tester_access_token: str
):
    response = await client.get(
        "/api/v1/product/get-by-subcategory-id",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_sub_category_id_without_id(
    client: AsyncClient, tester_access_token: str
):
    response = await client.get(
        "/api/v1/product/get-by-subcategory-id",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
