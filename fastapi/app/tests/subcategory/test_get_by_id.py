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
async def test_get_sub_category_by_id(
    client: AsyncClient,
    category_data: dict,
    sub_category_data: dict,
    tester_access_token: str,
):
    response = await client.post(
        "/api/v1/category/create",
        json=category_data,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_201_CREATED
    assert response_json["name"] == category_data["name"]

    category_id = response_json["id"]
    sub_category_data["category_id"] = category_id
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
    response = await client.get(
        f"/api/v1/subcategory/get-by-id/{subcategory_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == subcategory_id

    response = await client.delete(
        f"/api/v1/subcategory/{subcategory_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == subcategory_id

    response = await client.delete(
        f"/api/v1/category/{category_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == category_id


@pytest.mark.asyncio(loop_scope="session")
async def test_get_sub_category_by_invalid_id(
    client: AsyncClient, tester_access_token: str
):
    # Attempt to get a subcategory with an invalid ID (e.g., a string)
    invalid_subcategory_id = "invalid_id"
    response = await client.get(
        f"/api/v1/subcategory/get-by-id/{invalid_subcategory_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    logger.debug(response.json())
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_get_nonexistent_sub_category_by_id(
    client: AsyncClient, tester_access_token: str
):
    # Attempt to get a subcategory that doesn't exist
    nonexistent_subcategory_id = 99999  # Assuming this ID doesn't exist
    response = await client.get(
        f"/api/v1/subcategory/get-by-id/{nonexistent_subcategory_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    logger.debug(response.json())
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_get_sub_category_without_id(
    client: AsyncClient, tester_access_token: str
):
    # Attempt to get a subcategory without providing an ID
    response = await client.get(
        "/api/v1/subcategory/get-by-id",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    assert (
        response.status_code == HTTP_405_METHOD_NOT_ALLOWED
    )  # No route matching this


@pytest.mark.asyncio(loop_scope="session")
async def test_get_deleted_sub_category_by_id(
    client: AsyncClient,
    category_data: dict,
    sub_category_data: dict,
    tester_access_token: str,
):
    # Create category and subcategory
    response = await client.post(
        "/api/v1/category/create",
        json=category_data,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    category_id = response.json()["id"]
    sub_category_data["category_id"] = category_id

    response = await client.post(
        "/api/v1/subcategory/create",
        json=sub_category_data,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    subcategory_id = response.json()["id"]

    # Delete the subcategory
    response = await client.delete(
        f"/api/v1/subcategory/{subcategory_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    assert response.status_code == HTTP_200_OK

    # Attempt to get the deleted subcategory
    response = await client.get(
        f"/api/v1/subcategory/get-by-id/{subcategory_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    logger.debug(response.json())
    assert (
        response.status_code == HTTP_404_NOT_FOUND
    )  # Deleted subcategory should not be retrievable

    # Cleanup: Delete the category
    response = await client.delete(
        f"/api/v1/category/{category_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    assert response.status_code == HTTP_200_OK
