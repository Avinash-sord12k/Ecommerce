import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_category_id(
    client: AsyncClient,
    product: dict,
    tester_access_token: str,
):
    product_id = product["id"]
    category_id = product["category_id"]
    params = {"category_id": category_id, "page": 1, "page_size": 10}

    response = await client.get(
        "/api/v1/product/get-by-category-id",
        params=params,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK
    assert isinstance(response_json["items"], list)
    assert response_json["items"][0]["id"] == product_id
    assert response_json["total"] >= 1
    assert response_json["page"] == 1
    assert response_json["page_size"] == 10
    assert response_json["total_pages"] >= 1
    assert isinstance(response_json["has_next"], bool)
    assert isinstance(response_json["has_previous"], bool)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_invalid_category_id(
    client: AsyncClient, tester_access_token: str
):
    category_id = "12345"  # Assuming this is an invalid category ID
    params = {"page": 1, "page_size": 10}
    response = await client.get(
        "/api/v1/product/get-by-category-id",
        params={"category_id": category_id, **params},
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
    params = {"page": 1, "page_size": 10}
    response = await client.get(
        "/api/v1/product/get-by-category-id",
        params={"category_id": category_id, **params},
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_category_id_without_category_id(
    client: AsyncClient, tester_access_token: str
):
    params = {"page": 1, "page_size": 10}
    response = await client.get(
        "/api/v1/product/get-by-category-id",
        params=params,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
