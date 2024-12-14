from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from app.cart.models import (
    CartResponseModel,
    CreateCartRequestModel,
    AllCartsResponseModel,
    AddToCartRequestModel,
    SingleCartResponseModel,
)
from app.exceptions import EntityIntegrityError
from app.permissions.utils import allowed_permissions
from app.cart.repository import CartRepository
from app.users.utils import get_user_id_from_token

router = APIRouter(prefix="/api/v1/cart", tags=["Cart"])


@router.post(
    "/create",
    response_model=CartResponseModel,
    status_code=HTTP_201_CREATED,
    dependencies=[
        Depends(allowed_permissions(["create_cart"])),
    ],
)
async def create_cart(
    cart: CreateCartRequestModel,
    user_id: int = (Depends(get_user_id_from_token)),
):
    try:
        repo = CartRepository()
        new_cart_id = await repo.create(user_id, cart=cart)
        return JSONResponse(content=new_cart_id, status_code=HTTP_201_CREATED)
    except EntityIntegrityError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating cart: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/{id}",
    response_model=SingleCartResponseModel,
    status_code=HTTP_201_CREATED,
    dependencies=[
        Depends(allowed_permissions(["get_cart"])),
    ],
)
async def get_cart(id: int, user_id: int = (Depends(get_user_id_from_token))):
    try:
        repo = CartRepository()
        cart = await repo.get(user_id, cart_id=id)
        return JSONResponse(content=cart, status_code=HTTP_201_CREATED)
    except EntityIntegrityError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting cart: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/all",
    response_model=AllCartsResponseModel,
    status_code=HTTP_201_CREATED,
    dependencies=[
        Depends(allowed_permissions(["get_all_carts"])),
    ],
)
async def get_all_carts(user_id: int = (Depends(get_user_id_from_token))):
    try:
        repo = CartRepository()
        carts = await repo.get_all(user_id)
        return JSONResponse(content=carts, status_code=HTTP_201_CREATED)
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
)
async def delete_cart(
    id: int, user_id: int = (Depends(get_user_id_from_token))
):
    try:
        repo = CartRepository()
        await repo.delete(user_id, cart_id=id)
        return JSONResponse(content={}, status_code=HTTP_200_OK)
    except EntityIntegrityError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting cart: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.put(
    "/{id}",
    response_model=CartResponseModel,
    status_code=HTTP_200_OK,
    dependencies=[
        Depends(allowed_permissions(["update_cart"])),
    ],
)
async def update_cart(
    id: int,
    cart: CreateCartRequestModel,
    user_id: int = (Depends(get_user_id_from_token)),
):
    try:
        repo = CartRepository()
        updated_cart_id = await repo.update(user_id, cart_id=id, cart=cart)
        return JSONResponse(
            content=updated_cart_id, status_code=HTTP_201_CREATED
        )
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
        Depends(allowed_permissions(["add_item_to_cart"])),
    ],
)
async def add_item_to_cart(
    id: int,
    item: AddToCartRequestModel,
    user_id: int = (Depends(get_user_id_from_token)),
):
    try:
        repo = CartRepository()
        updated_cart_id = await repo.add_item(user_id, cart_id=id, item=item)
        return JSONResponse(
            content=updated_cart_id, status_code=HTTP_201_CREATED
        )
    except EntityIntegrityError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error adding item to cart: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)
