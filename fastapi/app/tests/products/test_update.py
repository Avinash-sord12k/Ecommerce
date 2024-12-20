import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product(
    client: AsyncClient,
    product: dict,
    product_data: dict,
    tester_access_token: str,
):
    product_id = product["id"]

    updated_product_data = {
        **product_data,
        "name": "Updated Product Name",
        "price": (
            int(product_data["price"])
            if isinstance(product_data["price"], str)
            else product_data["price"]
        ),
        "discount": (
            int(product_data["discount"])
            if isinstance(product_data["discount"], str)
            else product_data["discount"]
        ),
        "tax": (
            float(product_data["tax"])
            if isinstance(product_data["tax"], str)
            else product_data["tax"]
        ),
        "stock": (
            int(product_data["stock"])
            if isinstance(product_data["stock"], str)
            else product_data["stock"]
        ),
    }

    response = await client.put(
        f"/api/v1/product/update/{product_id}",
        json=updated_product_data,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(f"Request data: {updated_product_data}")
    logger.debug(f"Response status: {response.status_code}")
    logger.debug(f"Response data: {response_json}")
    assert response.status_code == HTTP_200_OK
    assert response_json["name"] == updated_product_data["name"]


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product_without_id(
    client: AsyncClient, tester_access_token: str
):
    response = await client.put(
        "/api/v1/product/update",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product_without_product_data(
    client: AsyncClient, product: dict, tester_access_token: str
):
    product_id = product["id"]
    response = await client.put(
        f"/api/v1/product/update/{product_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product_with_invalid_id(
    client: AsyncClient, tester_access_token: str
):
    product_id = "12345"  # Assuming this is an invalid product ID
    response = await client.put(
        f"/api/v1/product/update/{product_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product_with_non_existent_id(
    client: AsyncClient,
    product: str,
    product_data: dict,
    tester_access_token: str,
):
    product_data["name"] = "Updated Product Name"

    product_id = 99999999  # Assuming this is a non-existent product ID
    response = await client.put(
        f"/api/v1/product/update/{product_id}",
        json=product_data,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product_without_required_fields(
    client: AsyncClient,
    product: str,
    product_data: dict,
    tester_access_token: str,
):
    product_id = product
    product_data["name"] = ""

    response = await client.put(
        f"/api/v1/product/update/{product_id}",
        json=product_data,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
