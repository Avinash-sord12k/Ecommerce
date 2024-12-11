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
async def test_update_product(
    client: AsyncClient,
    product: dict,
    product_data: dict,
    seller_access_token: str,
):
    product_id = product["id"]
    product_data["name"] = "Updated Product Name"

    response = await client.put(
        f"/api/v1/product/update/{product_id}",
        json=product_data,
        headers={"Authorization": f"Bearer {seller_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK
    assert response_json["name"] == product_data["name"]


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product_without_id(client: AsyncClient):
    response = await client.put("/api/v1/product/update")
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product_without_product_data(
    client: AsyncClient, product: dict, seller_access_token: str
):
    product_id = product["id"]
    response = await client.put(
        f"/api/v1/product/update/{product_id}",
        headers={"Authorization": f"Bearer {seller_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product_with_invalid_id(
    client: AsyncClient, seller_access_token: str
):
    product_id = "12345"  # Assuming this is an invalid product ID
    response = await client.put(
        f"/api/v1/product/update/{product_id}",
        headers={"Authorization": f"Bearer {seller_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product_with_non_existent_id(
    client: AsyncClient,
    product: str,
    product_data: dict,
    seller_access_token: str,
):
    product_data["name"] = "Updated Product Name"

    product_id = 99999999  # Assuming this is a non-existent product ID
    response = await client.put(
        f"/api/v1/product/update/{product_id}",
        json=product_data,
        headers={"Authorization": f"Bearer {seller_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product_without_required_fields(
    client: AsyncClient,
    product: str,
    product_data: dict,
    seller_access_token: str,
):
    product_id = product
    product_data["name"] = ""

    response = await client.put(
        f"/api/v1/product/update/{product_id}",
        json=product_data,
        headers={"Authorization": f"Bearer {seller_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
