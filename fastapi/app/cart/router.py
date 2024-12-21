from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from app.cart.models import (
    AddToCartRequestModel,
    AllCartsResponseModel,
    CartResponseModel,
    CreateCartRequestModel,
    SingleCartResponseModel,
)
from app.cart.repository import CartRepository
from app.exceptions import EntityIntegrityError, EntityNotFoundError
from app.permissions.utils import allowed_permissions
from app.users.utils import get_current_user_id

router = APIRouter(prefix="/api/v1/cart", tags=["Cart"])


@router.post(
    "/create",
    response_model=CartResponseModel,
    status_code=HTTP_201_CREATED,
    dependencies=[
        Depends(allowed_permissions(["create_cart"])),
    ],
    openapi_extra={
        "security": [
            {"cookieAuth": [], "oauth2Auth": []},
        ]
    },
)
async def create_cart(
    cart: CreateCartRequestModel,
    user_id: int = (Depends(get_current_user_id)),
):
    try:
        repo = CartRepository()
        new_cart_id = await repo.create(user_id, cart=cart)
        return CartResponseModel(id=new_cart_id)
    except EntityIntegrityError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating cart: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/get-by-id/{id}",
    response_model=SingleCartResponseModel,
    status_code=HTTP_200_OK,
    dependencies=[
        Depends(allowed_permissions(["read_cart"])),
    ],
    openapi_extra={
        "security": [
            {"cookieAuth": [], "oauth2Auth": []},
        ]
    },
)
async def get_cart(id: int, user_id: int = (Depends(get_current_user_id))):
    try:
        repo = CartRepository()
        cart = await repo.get(user_id, cart_id=id)
        return SingleCartResponseModel(**cart)
    except EntityIntegrityError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting cart: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/get-all",
    response_model=AllCartsResponseModel,
    status_code=HTTP_200_OK,
    dependencies=[
        Depends(allowed_permissions(["read_cart"])),
    ],
    openapi_extra={
        "security": [
            {"cookieAuth": [], "oauth2Auth": []},
        ]
    },
)
async def get_all_carts(user_id: int = (Depends(get_current_user_id))):
    try:
        repo = CartRepository()
        carts = await repo.get_all(user_id)
        return AllCartsResponseModel(carts=carts)
    except EntityIntegrityError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting all carts: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete(
    "/{id}",
    response_model=CartResponseModel,
    status_code=HTTP_200_OK,
    dependencies=[
        Depends(allowed_permissions(["delete_cart"])),
    ],
    openapi_extra={
        "security": [
            {"cookieAuth": [], "oauth2Auth": []},
        ]
    },
)
async def delete_cart(id: int, user_id: int = (Depends(get_current_user_id))):
    try:
        repo = CartRepository()
        cart_id = await repo.delete(user_id, cart_id=id)
        return CartResponseModel(id=cart_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except EntityIntegrityError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting cart: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.put(
    "/update/{id}",
    response_model=CartResponseModel,
    status_code=HTTP_200_OK,
    dependencies=[
        Depends(allowed_permissions(["update_cart"])),
    ],
    openapi_extra={
        "security": [
            {"cookieAuth": [], "oauth2Auth": []},
        ]
    },
)
async def update_cart(
    id: int,
    cart: CreateCartRequestModel,
    user_id: int = (Depends(get_current_user_id)),
):
    try:
        repo = CartRepository()
        updated_cart_id = await repo.update(user_id, cart_id=id, cart=cart)
        return CartResponseModel(id=updated_cart_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except EntityIntegrityError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating cart: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.post(
    "/add-item",
    response_model=CartResponseModel,
    status_code=HTTP_200_OK,
    dependencies=[
        Depends(allowed_permissions(["update_cart"])),
    ],
    openapi_extra={
        "security": [
            {"cookieAuth": [], "oauth2Auth": []},
        ]
    },
)
async def add_item_to_cart(
    item: AddToCartRequestModel,
    user_id: int = (Depends(get_current_user_id)),
):
    try:
        repo = CartRepository()
        updated_cart_id = await repo.add_item(user_id, item=item)
        return CartResponseModel(id=updated_cart_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except EntityIntegrityError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error adding item to cart: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete(
    "/remove-item/{cart_id}/{product_id}",
    response_model=CartResponseModel,
    status_code=HTTP_200_OK,
    dependencies=[
        Depends(allowed_permissions(["update_cart"])),
    ],
    openapi_extra={
        "security": [
            {"cookieAuth": [], "oauth2Auth": []},
        ]
    },
)
async def remove_item_from_cart(
    cart_id: int,
    product_id: int,
    user_id: int = (Depends(get_current_user_id)),
):
    try:
        repo = CartRepository()
        updated_cart_id = await repo.remove_item(
            user_id, cart_id=cart_id, product_id=product_id
        )
        return CartResponseModel(id=updated_cart_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except EntityIntegrityError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error removing item from cart: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)
