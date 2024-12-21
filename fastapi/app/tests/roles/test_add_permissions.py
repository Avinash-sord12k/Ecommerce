import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_add_permission_to_role(
    client: AsyncClient, role: dict, tester_access_token: str
):
    # Update role with new permissions
    update_data = {"permissions": ["read_role"]}

    response = await client.put(
        f"/api/v1/role/update/{role['id']}",
        json=update_data,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(f"Response JSON: {response_json}")
    logger.debug(f"Response Status: {response.status_code}")
    assert response.status_code == HTTP_200_OK
    assert "read_role" in response_json["permissions"]


@pytest.mark.asyncio(loop_scope="session")
async def test_add_invalid_permission_to_role(
    client: AsyncClient, role: dict, tester_access_token: str
):
    # Try to update role with invalid permission
    update_data = {"permissions": ["invalid_permission"]}

    response = await client.put(
        f"/api/v1/role/update/{role['id']}",
        json=update_data,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_add_permission_to_nonexistent_role(
    client: AsyncClient, tester_access_token: str
):
    nonexistent_role_id = 99999  # Assuming this ID doesn't exist
    update_data = {"permissions": ["read_role"]}

    response = await client.put(
        f"/api/v1/role/update/{nonexistent_role_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_add_permission_to_role_without_permission(
    client: AsyncClient,
    role: dict,
    customer_access_token: str,
    seller_access_token: str,
):
    update_data = {"permissions": ["read_role"]}

    # Test with customer token
    response = await client.put(
        f"/api/v1/role/update/{role['id']}",
        json=update_data,
        headers={"Authorization": f"Bearer {customer_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_403_FORBIDDEN

    # Test with seller token
    response = await client.put(
        f"/api/v1/role/update/{role['id']}",
        json=update_data,
        headers={"Authorization": f"Bearer {seller_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.asyncio(loop_scope="session")
async def test_add_duplicate_permissions_to_role(
    client: AsyncClient, role: dict, tester_access_token: str
):
    # Update with duplicate permissions
    update_data = {
        "permissions": ["read_role", "read_role"]  # Duplicate permission
    }

    response = await client.put(
        f"/api/v1/role/update/{role['id']}",
        json=update_data,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(f"Response JSON: {response_json}")
    logger.debug(f"Response Status: {response.status_code}")
    assert response.status_code == HTTP_200_OK
    # Check that the permission appears only once
    assert response_json["permissions"].count("read_role") == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_clear_role_permissions(
    client: AsyncClient, role: dict, tester_access_token: str
):
    # First add some permissions
    update_data = {"permissions": ["read_role"]}

    response = await client.put(
        f"/api/v1/role/update/{role['id']}",
        json=update_data,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(f"First update response: {response_json}")
    assert response.status_code == HTTP_200_OK
    assert "read_role" in response_json["permissions"]

    # Then clear the permissions
    update_data["permissions"] = []
    response = await client.put(
        f"/api/v1/role/update/{role['id']}",
        json=update_data,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(f"Clear permissions response: {response_json}")
    assert response.status_code == HTTP_200_OK
    assert not response_json["permissions"]  # Permissions should be empty
