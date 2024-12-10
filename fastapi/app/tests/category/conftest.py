from uuid import uuid4

import pytest_asyncio


@pytest_asyncio.fixture(scope="session")
def category_data():
    """Fixture to provide category data."""
    return {"name": str(uuid4())}
