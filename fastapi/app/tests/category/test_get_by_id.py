import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_category_by_id(
    client: AsyncClient, category_id: str, admin_access_token: str
):
    # Get category by ID
    response = await client.get(
        f"/api/v1/category/get-by-id/{category_id}",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == category_id


@pytest.mark.asyncio(loop_scope="session")
async def test_get_category_by_id_not_admin(
    client: AsyncClient,
    category_id: str,
    customer_access_token: str,
    seller_access_token: str,
):
    # Get category by ID
    response = await client.get(
        f"/api/v1/category/get-by-id/{category_id}",
        headers={"Authorization": f"Bearer {customer_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK

    response = await client.get(
        f"/api/v1/category/get-by-id/{category_id}",
        headers={"Authorization": f"Bearer {seller_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK


@pytest.mark.asyncio(loop_scope="session")
async def test_get_nonexistent_category_by_id(
    client: AsyncClient, admin_access_token: str
):
    nonexistent_category_id = 99999  # Assuming 99999 doesn't exist
    response = await client.get(
        f"/api/v1/category/get-by-id/{nonexistent_category_id}",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_get_category_by_invalid_id(
    client: AsyncClient, admin_access_token: str
):
    invalid_category_id = "invalid_id"
    response = await client.get(
        f"/api/v1/category/get-by-id/{invalid_category_id}",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
