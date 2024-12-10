from uuid import uuid4

import pytest_asyncio


@pytest_asyncio.fixture(scope="session")
def role_data():
    """Fixture to provide role data."""
    return {"name": str(uuid4()), "description": str(uuid4())}
