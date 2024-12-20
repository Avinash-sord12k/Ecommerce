import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import HTTP_200_OK, HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_get_products(
    client: AsyncClient, product: dict, tester_access_token: str
):
    response = await client.get(
        "/api/v1/product",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK
    assert response_json["total"] > 0
    assert len(response_json["items"]) > 0


@pytest.mark.asyncio(loop_scope="session")
async def test_get_products_with_filters(
    client: AsyncClient, product: dict, tester_access_token: str
):
    response = await client.get(
        "/api/v1/product",
        params={
            "min_price": 10,
            "max_price": 1000,
            "category_id": product["category_id"],
            "is_active": True,
            "sort_by": "price",
            "sort_order": "asc",
        },
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    assert response.status_code == HTTP_200_OK

    response_json = response.json()
    logger.debug(response_json)

    if response_json["total"] > 0:
        items = response_json["items"]
        assert all(10 <= float(item["price"]) <= 1000 for item in items)
        assert all(
            item["category_id"] == product["category_id"] for item in items
        )
        assert all(item["is_active"] for item in items)

        # Verify price sorting
        prices = [float(item["price"]) for item in items]
        assert prices == sorted(prices)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_products_with_pagination(
    client: AsyncClient, product: dict, tester_access_token: str
):
    response = await client.get(
        "/api/v1/product",
        params={"page": 1, "page_size": 5},
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    assert response.status_code == HTTP_200_OK

    response_json = response.json()
    logger.debug(response_json)

    assert len(response_json["items"]) <= 5
    assert response_json["page"] == 1
    assert response_json["page_size"] == 5
    assert response_json["total_pages"] >= 1


@pytest.mark.asyncio(loop_scope="session")
async def test_get_products_with_search(
    client: AsyncClient, product: dict, tester_access_token: str
):
    response = await client.get(
        "/api/v1/product",
        params={"search": product["name"]},
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    assert response.status_code == HTTP_200_OK

    response_json = response.json()
    logger.debug(f"Search term: {product['name']}")
    logger.debug("Response items:")
    for item in response_json["items"]:
        logger.debug(f"Item name: {item['name']}")

    if response_json["total"] > 0:
        assert any(
            product["name"].lower() in item["name"].lower()
            for item in response_json["items"]
        )


@pytest.mark.asyncio(loop_scope="session")
async def test_get_products_invalid_sort(
    client: AsyncClient, tester_access_token: str
):
    response = await client.get(
        "/api/v1/product",
        params={"sort_by": "invalid", "sort_order": "desc"},
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    response_json = response.json()
    logger.debug(response_json)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_products_invalid_pagination(
    client: AsyncClient, tester_access_token: str
):
    response = await client.get(
        "/api/v1/product",
        params={"page": 0, "page_size": -1},
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
