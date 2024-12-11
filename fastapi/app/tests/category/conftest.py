from uuid import uuid4

import pytest_asyncio
from httpx import AsyncClient


@pytest_asyncio.fixture(scope="session")
def category_data():
    """Fixture to provide category data."""
    return {"name": str(uuid4())}


@pytest_asyncio.fixture(scope="session")
async def admin_access_token(client: AsyncClient):
    login_data = {"username": "admin", "password": "admin123"}
    response = await client.post("/api/v1/users/login", data=login_data)
    return response.json()["access_token"]


@pytest_asyncio.fixture(scope="session")
async def customer_access_token(client: AsyncClient):
    login_data = {"username": "customer", "password": "customer123"}
    response = await client.post("/api/v1/users/login", data=login_data)
    return response.json()["access_token"]


@pytest_asyncio.fixture(scope="session")
async def seller_access_token(client: AsyncClient):
    login_data = {"username": "seller", "password": "seller123"}
    response = await client.post("/api/v1/users/login", data=login_data)
    return response.json()["access_token"]


@pytest_asyncio.fixture(scope="session")
async def category_id(
    client: AsyncClient, category_data: dict, admin_access_token: str
):
    # Create category
    response = await client.post(
        "/api/v1/category/create",
        json=category_data,
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    response_json = response.json()
    category_id = response_json["id"]
    yield category_id

    # Delete category
    response = await client.delete(
        f"/api/v1/category/{category_id}",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    response_json = response.json()
    return
