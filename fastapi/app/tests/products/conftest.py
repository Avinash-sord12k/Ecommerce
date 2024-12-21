from uuid import uuid4

import pytest_asyncio
from httpx import AsyncClient
from starlette.status import HTTP_200_OK, HTTP_201_CREATED


@pytest_asyncio.fixture(scope="session")
def category_data():
    """Fixture to provide category data."""
    return {"name": str(uuid4())}


@pytest_asyncio.fixture(scope="session")
def sub_category_data():
    """Fixture to provide category data."""
    return {"name": str(uuid4()), "category_id": None}


@pytest_asyncio.fixture(scope="session")
def product_data():
    """Fixture to provide product data."""
    return {
        "name": str(uuid4()),
        "description": str(uuid4()),
        "price": 80000,
        "slug": str(uuid4()),
        "tags": str(uuid4()),
        "discount": 5,
        "tax": 18,
        "stock": 300,
        "category_id": None,
        "sub_category_id": None,
        "is_active": True,
    }


@pytest_asyncio.fixture(scope="session")
async def category(
    client: AsyncClient, category_data: dict, tester_access_token: str
):
    # Create category
    response = await client.post(
        "/api/v1/category/create",
        json=category_data,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    assert response.status_code == HTTP_201_CREATED
    assert response_json["name"] == category_data["name"]

    category_id = response_json["id"]
    yield category_id  # Return the category ID to the test

    # Cleanup: Delete category
    response = await client.delete(
        f"/api/v1/category/{category_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == category_id


@pytest_asyncio.fixture(scope="session")
async def sub_category(
    client: AsyncClient,
    category: str,
    sub_category_data: dict,
    tester_access_token: str,
):
    # Create subcategory
    sub_category_data["category_id"] = category
    response = await client.post(
        "/api/v1/subcategory/create",
        json=sub_category_data,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    assert response.status_code == HTTP_201_CREATED
    assert response_json["name"] == sub_category_data["name"]

    subcategory_id = response_json["id"]
    yield category, subcategory_id  # Return the subcategory ID and category ID to the test

    # Cleanup: Delete subcategory
    response = await client.delete(
        f"/api/v1/subcategory/{subcategory_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == subcategory_id


@pytest_asyncio.fixture(scope="session")
async def product(
    client: AsyncClient,
    sub_category: tuple,
    product_data: dict,
    tester_access_token: str,
):
    category_id, subcategory_id = sub_category
    product_data["category_id"] = category_id
    product_data["sub_category_ids"] = [subcategory_id]

    response = await client.post(
        "/api/v1/product/create",
        json=product_data,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    assert response.status_code == HTTP_201_CREATED
    assert response_json["name"] == product_data["name"]
    yield response_json

    # Cleanup: Delete product
    product_id = response_json["id"]
    response = await client.delete(
        f"/api/v1/product/{product_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == product_id
