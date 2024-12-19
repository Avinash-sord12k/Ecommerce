from math import ceil

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from app.exceptions import EntityIntegrityError, EntityNotFoundError
from app.models import PaginatedResponse, PaginationParams
from app.permissions.utils import allowed_permissions
from app.products.models import (
    CreateProductRequestModel,
    ProductResponseModel,
    UpdateProductRequestModel,
)
from app.products.repository import ProductRepository
from app.users.utils import get_user_id_from_token, oauth2scheme

router = APIRouter(prefix="/api/v1/product", tags=["Product"])


@router.post(
    "/create",
    response_model=ProductResponseModel,
    status_code=HTTP_201_CREATED,
    dependencies=[
        Depends(oauth2scheme),
        Depends(allowed_permissions(["create_product"])),
    ],
)
async def create_product(
    product: CreateProductRequestModel,
    user_id: int = Depends(get_user_id_from_token),
):
    try:
        repo = ProductRepository()
        new_product_id = await repo.create(user_id, product)
        return JSONResponse(
            content={
                "id": new_product_id,
                "user_id": user_id,
                **product.model_dump(),
            },
            status_code=HTTP_201_CREATED,
        )
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except EntityIntegrityError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating product: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/get-by-id/{id}",
    response_model=PaginatedResponse[ProductResponseModel],
    status_code=HTTP_200_OK,
    dependencies=[
        Depends(oauth2scheme),
        Depends(allowed_permissions(["read_product"])),
    ],
)
async def get_product_by_id(id: int, pagination: PaginationParams = Depends()):
    try:
        repo = ProductRepository()
        product = await repo.get_by_id(id)
        return JSONResponse(content=product, status_code=HTTP_200_OK)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting product by id: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/get-by-category-id",
    response_model=PaginatedResponse[ProductResponseModel],
    status_code=HTTP_200_OK,
    dependencies=[
        Depends(oauth2scheme),
        Depends(allowed_permissions(["read_product"])),
    ],
)
async def get_product_by_category_id(
    category_id: int, pagination: PaginationParams = Depends()
):
    try:
        repo = ProductRepository()
        products, total = await repo.get_by_category_id(
            category_id, pagination.page, pagination.page_size
        )

        total_pages = ceil(total / pagination.page_size)

        return PaginatedResponse(
            items=products,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            total_pages=total_pages,
        )
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting products by category: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/get-by-subcategory-id",
    response_model=PaginatedResponse[ProductResponseModel],
    status_code=HTTP_200_OK,
    dependencies=[
        Depends(oauth2scheme),
        Depends(allowed_permissions(["read_product"])),
    ],
)
async def get_product_by_sub_category_id(
    sub_category_id: int, pagination: PaginationParams = Depends()
):
    try:
        repo = ProductRepository()
        products, total = await repo.get_by_subcategory_id(
            sub_category_id, pagination.page, pagination.page_size
        )

        total_pages = ceil(total / pagination.page_size)

        return PaginatedResponse(
            items=products,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            total_pages=total_pages,
        )
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting products by sub-category id: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.put(
    "/update/{id}",
    response_model=ProductResponseModel,
    status_code=HTTP_200_OK,
    dependencies=[
        Depends(oauth2scheme),
        Depends(allowed_permissions(["update_product"])),
    ],
)
async def update_product(id: int, product: UpdateProductRequestModel):
    try:
        repo = ProductRepository()
        product = await repo.update(id, product)
        return JSONResponse(content=product, status_code=HTTP_200_OK)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating product: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete(
    "/{id}",
    response_model=ProductResponseModel,
    status_code=HTTP_200_OK,
    dependencies=[
        Depends(oauth2scheme),
        Depends(allowed_permissions(["delete_product"])),
    ],
)
async def delete_product(id: int):
    try:
        repo = ProductRepository()
        product = await repo.delete(id)
        return JSONResponse(content=product, status_code=HTTP_200_OK)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting product: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)
