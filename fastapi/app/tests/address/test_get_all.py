import pytest
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all(
    client: AsyncClient, address: dict, tester_access_token: str
):
    response = await client.get(
        "/api/v1/address/get-all",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    assert response.status_code == HTTP_200_OK
    response_data = response.json()

    assert "items" in response_data
    assert "total" in response_data
    assert "page" in response_data
    assert "page_size" in response_data
    assert "total_pages" in response_data
    assert "has_next" in response_data
    assert "has_previous" in response_data

    assert any(item["id"] == address["id"] for item in response_data["items"])


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_with_pagination(
    client: AsyncClient, address: dict, tester_access_token: str
):
    response = await client.get(
        "/api/v1/address/get-all?page=1&page_size=5",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    assert response.status_code == HTTP_200_OK
    response_data = response.json()
    assert response_data["page"] == 1
    assert response_data["page_size"] == 5


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_with_address_id(
    client: AsyncClient, address: dict, tester_access_token: str
):
    address_id = address["id"]
    response = await client.get(
        f"/api/v1/address/get-all?address_id={address_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    assert response.status_code == HTTP_200_OK
    response_data = response.json()
    assert len(response_data["items"]) == 1
    assert response_data["items"][0]["id"] == address_id


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_with_invalid_page(
    client: AsyncClient, tester_access_token: str
):
    response = await client.get(
        "/api/v1/address/get-all?page=0",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_with_invalid_page_size(
    client: AsyncClient, tester_access_token: str
):
    response = await client.get(
        "/api/v1/address/get-all?page_size=101",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_without_permission(
    client: AsyncClient, admin_access_token: str
):
    response = await client.get(
        "/api/v1/address/get-all",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == HTTP_403_FORBIDDEN
