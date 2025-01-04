import time

import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_roles(
    client: AsyncClient, role: dict, tester_access_token: str
):
    """Test basic role listing with pagination verification"""
    response = await client.get(
        "/api/v1/role",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK

    # Verify pagination fields
    assert "total" in response_json
    assert "page" in response_json
    assert "page_size" in response_json
    assert "total_pages" in response_json
    assert "has_next" in response_json
    assert "has_previous" in response_json

    role_id = role["id"]
    all_roles = response_json["items"]
    matching_role = next((r for r in all_roles if r["id"] == role_id), None)
    assert matching_role is not None
    assert "permissions" in matching_role
    assert (
        matching_role["permissions"] == []
    )  # Verify empty permissions by default


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_roles_no_admin(
    client: AsyncClient,
    role: dict,
    customer_access_token: str,
    seller_access_token: str,
):
    """Test role listing access for non-admin users"""
    response = await client.get(
        "/api/v1/role",
        headers={"Authorization": f"Bearer {customer_access_token}"},
    )
    assert response.status_code == HTTP_200_OK
    role_id = role["id"]
    all_roles = response.json()["items"]

    matching_role = next((r for r in all_roles if r["id"] == role_id), None)
    assert matching_role is not None

    response = await client.get(
        "/api/v1/role",
        headers={"Authorization": f"Bearer {seller_access_token}"},
    )
    assert response.status_code == HTTP_200_OK
    all_roles = response.json()["items"]

    matching_role = next((r for r in all_roles if r["id"] == role_id), None)
    assert matching_role is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_roles_pagination(
    client: AsyncClient, role: dict, tester_access_token: str
):
    """Test pagination functionality and role_id filtering"""
    # Test pagination
    response = await client.get(
        "/api/v1/role?page=1&page_size=2",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK

    # Verify pagination
    assert response_json["page"] == 1
    assert response_json["page_size"] == 2
    assert len(response_json["items"]) <= 2

    # Test with role_id filter
    response = await client.get(
        f"/api/v1/role?role_id={role['id']}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK

    all_roles = response_json["items"]
    assert all(r["id"] >= role["id"] for r in all_roles)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_roles_with_permissions(
    client: AsyncClient, role: dict, tester_access_token: str
):
    """Test role listing with permissions included"""
    # Test with permissions included
    response = await client.get(
        "/api/v1/role?include_permissions=true",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK

    all_roles = response_json["items"]
    for role_item in all_roles:
        assert "permissions" in role_item
        assert isinstance(role_item["permissions"], list)

    # Test with both role_id and permissions
    response = await client.get(
        f"/api/v1/role?role_id={role['id']}&include_permissions=true",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK

    all_roles = response_json["items"]
    assert all(r["id"] >= role["id"] for r in all_roles)
    for role_item in all_roles:
        assert "permissions" in role_item
        assert isinstance(role_item["permissions"], list)
        assert "name" in role_item
        assert "description" in role_item
        assert isinstance(role_item["id"], int)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_roles_invalid_params(
    client: AsyncClient, tester_access_token: str
):
    """Test invalid parameter handling"""
    # Test invalid page number
    response = await client.get(
        "/api/v1/role?page=0",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    # Test invalid page size
    response = await client.get(
        "/api/v1/role?page_size=0",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    # Test page size exceeding maximum
    response = await client.get(
        "/api/v1/role?page_size=101",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_roles_empty_results(
    client: AsyncClient, tester_access_token: str
):
    """Test cases that should return empty results"""
    response = await client.get(
        "/api/v1/role?role_id=999999",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(response_json["items"]) == 0
    assert response_json["total"] == 0
    assert response_json["total_pages"] == 0


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_roles_performance(
    client: AsyncClient, tester_access_token: str
):
    """Test response time for different scenarios"""
    # Test basic request
    start_time = time.time()
    response = await client.get(
        "/api/v1/role",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    basic_time = time.time() - start_time
    assert basic_time < 1.0  # Response should be under 1 second

    # Test with permissions
    start_time = time.time()
    response = await client.get(
        "/api/v1/role?include_permissions=true",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    permission_time = time.time() - start_time
    assert permission_time < 1.5  # Response should be under 1.5 seconds
