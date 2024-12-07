import pytest_asyncio
from uuid import uuid4


@pytest_asyncio.fixture(scope="session")
def category_data():
    """Fixture to provide category data."""
    return {"name": str(uuid4())}


@pytest_asyncio.fixture(scope="session")
def sub_category_data():
    """Fixture to provide category data."""
    return {"name": str(uuid4())}
