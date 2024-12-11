import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_sub_category(
    client: AsyncClient,
    category: int,
    sub_category_data: dict,
    tester_access_token: str,
):
    sub_category_data["category_id"] = category
    response = await client.post(
        "/api/v1/subcategory/create",
        json=sub_category_data,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_201_CREATED
    assert response_json["name"] == sub_category_data["name"]

    subcategory_id = response_json["id"]
    logger.debug(f"{subcategory_id=}")
    response = await client.delete(
        f"/api/v1/subcategory/{subcategory_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == subcategory_id


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_nonexistent_sub_category(
    client: AsyncClient, tester_access_token: str
):
    # Try to delete a subcategory that doesn't exist
    nonexistent_subcategory_id = 99999  # Assuming this ID doesn't exist
    response = await client.delete(
        f"/api/v1/subcategory/{nonexistent_subcategory_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    logger.debug(response.json())
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_sub_category_without_id(
    client: AsyncClient, tester_access_token: str
):
    # Try to delete a subcategory without providing an ID
    response = await client.delete(
        "/api/v1/subcategory/",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    logger.debug(response.json())
    assert (
        response.status_code == HTTP_404_NOT_FOUND
    )  # Route not found for empty ID


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_sub_category_with_invalid_id(
    client: AsyncClient, tester_access_token: str
):
    # Try to delete a subcategory with an invalid ID (e.g., a string instead of an integer)
    invalid_subcategory_id = "invalid_id"
    response = await client.delete(
        f"/api/v1/subcategory/{invalid_subcategory_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    logger.debug(response.json())
    assert (
        response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    )  # Assuming invalid ID results in "not found"


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_sub_category_twice(
    client: AsyncClient,
    category: int,
    sub_category_data: dict,
    tester_access_token: str,
):
    sub_category_data["category_id"] = category
    response = await client.post(
        "/api/v1/subcategory/create",
        json=sub_category_data,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    assert response.status_code == HTTP_201_CREATED
    subcategory_id = response.json()["id"]

    # Delete the subcategory the first time
    response = await client.delete(
        f"/api/v1/subcategory/{subcategory_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    logger.debug(response.json())
    assert response.status_code == HTTP_200_OK

    # Try deleting the same subcategory again
    response = await client.delete(
        f"/api/v1/subcategory/{subcategory_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    logger.debug(response.json())
    assert (
        response.status_code == HTTP_404_NOT_FOUND
    )  # Subcategory no longer exists
