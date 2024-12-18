import pytest
from httpx import AsyncClient
from starlette.status import HTTP_200_OK


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all(
    client: AsyncClient, address: dict, tester_access_token: str
):
    response = await client.get(
        "/api/v1/address/get-all",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    assert response.status_code == HTTP_200_OK


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_without_creation(
    client: AsyncClient, tester_access_token: str
):
    response = await client.get(
        "/api/v1/address/get-all",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    assert response.status_code == HTTP_200_OK
    assert len(response.json()["addresses"]) == 0
