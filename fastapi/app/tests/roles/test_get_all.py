import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_roles(
    client: AsyncClient, role: dict, tester_access_token: str
):
    response = await client.get(
        "/api/v1/role/get-all",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK

    role_id = role["id"]
    all_roles = response_json["roles"]

    matching_role = next((r for r in all_roles if r["id"] == role_id), None)
    assert matching_role is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_roles_no_admin(
    client: AsyncClient,
    role: dict,
    customer_access_token: str,
    seller_access_token: str,
):
    response = await client.get(
        "/api/v1/role/get-all",
        headers={"Authorization": f"Bearer {customer_access_token}"},
    )
    assert response.status_code == HTTP_200_OK

    response = await client.get(
        "/api/v1/role/get-all",
        headers={"Authorization": f"Bearer {seller_access_token}"},
    )
    assert response.status_code == HTTP_200_OK
