import pytest_asyncio


@pytest_asyncio.fixture(scope="session")
def category_data():
    """Fixture to provide category data."""
    return {"name": "Category 1"}
