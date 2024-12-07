import pytest
from httpx import AsyncClient
from loguru import logger
from starlette.status import HTTP_200_OK, HTTP_201_CREATED


@pytest.mark.asyncio(loop_scope="session")
async def test_create_sub_category(client: AsyncClient, category_data: dict, sub_category_data: dict):
    response = await client.post("/api/v1/category/create", json=category_data)
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_201_CREATED
    assert response_json["name"] == category_data["name"]

    category_id = response_json["id"]
    sub_category_data["category_id"] = category_id
    response = await client.post("/api/v1/subcategory/create", json=sub_category_data)
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_201_CREATED
    assert response_json["name"] == sub_category_data["name"]

    subcategory_id = response_json["id"]
    logger.debug(f"{subcategory_id=}")
    response = await client.delete(f"/api/v1/subcategory/{subcategory_id}")
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == subcategory_id

    logger.debug(f"{category_id=}")
    response = await client.delete(f"/api/v1/category/{category_id}")
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == category_id
