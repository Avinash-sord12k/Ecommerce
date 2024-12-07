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
