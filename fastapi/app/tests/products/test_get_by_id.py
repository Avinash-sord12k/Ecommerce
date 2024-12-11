import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_id(
    client: AsyncClient, product: dict, seller_access_token: str
):
    product_id = product["id"]
    response = await client.get(
        f"/api/v1/product/get-by-id/{product_id}",
        headers={"Authorization": f"Bearer {seller_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == product_id


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_invalid_id(
    client: AsyncClient, seller_access_token: str
):
    product_id = "12345"  # Assuming this is an invalid product ID
    response = await client.get(
        f"/api/v1/product/get-by-id/{product_id}",
        headers={"Authorization": f"Bearer {seller_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_non_existent_id(
    client: AsyncClient, seller_access_token: str
):
    product_id = 12345  # Assuming this is a non-existent product ID
    response = await client.get(
        f"/api/v1/product/get-by-id/{product_id}",
        headers={"Authorization": f"Bearer {seller_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_id_without_id(
    client: AsyncClient, seller_access_token: str
):
    response = await client.get(
        "/api/v1/product/get-by-id",
        headers={"Authorization": f"Bearer {seller_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED
