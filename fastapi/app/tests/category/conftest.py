from uuid import uuid4

import pytest_asyncio
from httpx import AsyncClient


@pytest_asyncio.fixture(scope="module")
def category_data():
    """Fixture to provide category data."""
    return {"name": str(uuid4())}


@pytest_asyncio.fixture(scope="module")
async def category_id(
    client: AsyncClient, category_data: dict, tester_access_token: str
):
    # Create category
    response = await client.post(
        "/api/v1/category/create",
        json=category_data,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    category_id = response_json["id"]
    yield category_id

    # Delete category
    response = await client.delete(
        f"/api/v1/category/{category_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    return
