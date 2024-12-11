import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_category_id(
    client: AsyncClient,
    product: dict,
    tester_access_token: str,
):
    product_id = product["id"]
    category_id = product["category_id"]

    response = await client.get(
        f"/api/v1/product/get-by-category-id/{category_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK
    assert response_json[0]["id"] == product_id


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_invalid_category_id(
    client: AsyncClient, tester_access_token: str
):
    category_id = "12345"  # Assuming this is an invalid category ID
    response = await client.get(
        f"/api/v1/product/get-by-category-id/{category_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_non_existent_category_id(
    client: AsyncClient, tester_access_token: str
):
    category_id = 12345  # Assuming this is a non-existent category ID
    response = await client.get(
        f"/api/v1/product/get-by-category-id/{category_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_category_id_without_category_id(
    client: AsyncClient, tester_access_token: str
):
    response = await client.get(
        "/api/v1/product/get-by-category-id",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_category_id_without_id(
    client: AsyncClient, tester_access_token: str
):
    response = await client.get(
        "/api/v1/product/get-by-category-id",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED
