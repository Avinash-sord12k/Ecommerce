import pytest
import pytest_asyncio
from uuid import uuid4
from httpx import AsyncClient
from starlette.status import HTTP_200_OK, HTTP_201_CREATED


@pytest_asyncio.fixture(scope="module")
def category_data():
    """Fixture to provide category data."""
    return {"name": str(uuid4())}


@pytest_asyncio.fixture(scope="module")
def sub_category_data():
    """Fixture to provide category data."""
    return {"name": str(uuid4()), "category_id": None}


@pytest_asyncio.fixture(scope="module")
def product_data():
    """Fixture to provide product data."""
    return {
        "name": str(uuid4()),
        "description": str(uuid4()),
        "price": 80000,
        "slug": str(uuid4()),
        "tags": str(uuid4()),
        "discount": 5,
        "stock": 300,
        "category_id": None,
        "sub_category_id": None,
        "is_active": True,
    }


@pytest.fixture(scope="module")
async def category(client: AsyncClient, category_data: dict):
    # Create category
    response = await client.post("/api/v1/category/create", json=category_data)
    response_json = response.json()
    assert response.status_code == HTTP_201_CREATED
    assert response_json["name"] == category_data["name"]

    category_id = response_json["id"]
    yield category_id  # Return the category ID to the test

    # Cleanup: Delete category
    response = await client.delete(f"/api/v1/category/{category_id}")
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == category_id


@pytest.fixture(scope="module")
async def sub_category(
    client: AsyncClient, category: str, sub_category_data: dict
):
    # Create subcategory
    sub_category_data["category_id"] = category
    response = await client.post(
        "/api/v1/subcategory/create", json=sub_category_data
    )
    response_json = response.json()
    assert response.status_code == HTTP_201_CREATED
    assert response_json["name"] == sub_category_data["name"]

    subcategory_id = response_json["id"]
    yield category, subcategory_id  # Return the subcategory ID and category ID to the test

    # Cleanup: Delete subcategory
    response = await client.delete(f"/api/v1/subcategory/{subcategory_id}")
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == subcategory_id
