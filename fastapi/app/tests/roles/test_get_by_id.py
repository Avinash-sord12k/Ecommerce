import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import HTTP_200_OK


@pytest.mark.asyncio(loop_scope="session")
async def test_get_role_by_id(
    client: AsyncClient, role: dict, tester_access_token: str
):
    role_id = role["id"]
    response = await client.get(
        f"/api/v1/role/get-by-id/{role_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    logger.info(response.json())
    assert response.status_code == HTTP_200_OK


@pytest.mark.asyncio(loop_scope="session")
async def test_get_role_by_id_not_admin(
    client: AsyncClient,
    role: dict,
    customer_access_token: str,
    seller_access_token: str,
):
    role_id = role["id"]
    response = await client.get(
        f"/api/v1/role/get-by-id/{role_id}",
        headers={"Authorization": f"Bearer {customer_access_token}"},
    )
    assert response.status_code == HTTP_200_OK

    response = await client.get(
        f"/api/v1/role/get-by-id/{role_id}",
        headers={"Authorization": f"Bearer {seller_access_token}"},
    )
    assert response.status_code == HTTP_200_OK
