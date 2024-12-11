import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

from app.main import app

pytest_plugins = ("pytest_asyncio",)


@pytest_asyncio.fixture(scope="session")
async def lifespanned_app():
    async with LifespanManager(app) as manager:
        yield manager.app


@pytest_asyncio.fixture(scope="session")
async def client(lifespanned_app):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://0.0.0.0:5000",
    ) as _client:
        yield _client


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
async def tester_access_token(client: AsyncClient):
    login_data = {"username": "tester", "password": "tester123"}
    response = await client.post("/api/v1/users/login", data=login_data)
    return response.json()["access_token"]
