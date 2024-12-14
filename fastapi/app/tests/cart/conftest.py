import pytest_asyncio
from httpx import AsyncClient
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from loguru import logger

from app.cart.models import CreateCartRequestModel, AddToCartRequestModel


@pytest_asyncio.fixture(scope="module")
def create_cart_request_payload() -> dict:
    return CreateCartRequestModel(
        name="test cart",
        remainder_date="2099-01-01T00:00:00.000Z",
    ).model_dump()


@pytest_asyncio.fixture(scope="module")
def add_to_cart_request_payload() -> dict:
    return AddToCartRequestModel(
        product_id=1,
        quantity=1,
    ).model_dump()


@pytest_asyncio.fixture(scope="module")
async def cart(
    client: AsyncClient,
    create_cart_request_payload: dict,
    tester_access_token: str,
):
    response = await client.post(
        "/api/v1/cart/create",
        json=create_cart_request_payload,
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    assert response.status_code == HTTP_201_CREATED
    yield response_json

    cart_id = response_json["id"]
    response = await client.delete(
        f"/api/v1/cart/{cart_id}",
        headers={"Authorization": f"Bearer {tester_access_token}"},
    )
    response_json = response.json()
    logger.debug(response_json)
    assert response.status_code == HTTP_200_OK
