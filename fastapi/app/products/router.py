from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from app.exceptions import EntityNotFoundError
from app.products.repository import ProductRepository
from app.products.models import (
    CreateProductRequestSchema,
    ProductResponseSchema,
    UpdateProductRequestSchema,
)

router = APIRouter(prefix="/api/v1/product", tags=["Product"])


@router.post(
    "/create",
    response_model=ProductResponseSchema,
    status_code=HTTP_201_CREATED,
)
async def create_product(product: CreateProductRequestSchema):
    try:
        repo = ProductRepository()
        new_product_id = await repo.create(product)
        return ProductResponseSchema(id=new_product_id, **product.model_dump())
    except Exception as e:
        logger.error(f"Error creating product: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/get-by-id/{id}",
    response_model=ProductResponseSchema,
    status_code=HTTP_200_OK,
)
async def get_product_by_id(id: int):
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
    "/get-by-category-id/{category_id}",
    response_model=ProductResponseSchema,
    status_code=HTTP_200_OK,
)
async def get_product_by_category_id(category_id: int):
    try:
        repo = ProductRepository()
        products = await repo.get_by_category_id(category_id)
        return JSONResponse(content=products, status_code=HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error getting products by category: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/get-by-category-name/{category_name}",
    response_model=ProductResponseSchema,
    status_code=HTTP_200_OK,
)
async def get_product_by_category_name(category_name: str):
    try:
        repo = ProductRepository()
        products = await repo.get_by_category_name(category_name)
        return JSONResponse(content=products, status_code=HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error getting products by category name: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/get-by-subcategory-id/{sub_category_id}",
    response_model=ProductResponseSchema,
    status_code=HTTP_200_OK,
)
async def get_product_by_sub_category_id(sub_category_id: int):
    try:
        repo = ProductRepository()
        products = await repo.get_by_sub_category_id(sub_category_id)
        return JSONResponse(content=products, status_code=HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error getting products by sub-category id: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/get-by-subcategory-name/{sub_category_name}",
    response_model=ProductResponseSchema,
    status_code=HTTP_200_OK,
)
async def get_product_by_sub_category_name(sub_category_name: str):
    try:
        repo = ProductRepository()
        products = await repo.get_by_sub_category_name(sub_category_name)
        return JSONResponse(content=products, status_code=HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error getting products by sub-category name: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.put(
    "/update/{id}",
    response_model=ProductResponseSchema,
    status_code=HTTP_200_OK,
)
async def update_product(id: int, product: UpdateProductRequestSchema):
    try:
        repo = ProductRepository()
        product = await repo.update(id, product)
        return JSONResponse(content=product, status_code=HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error updating product: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{id}", response_model=ProductResponseSchema, status_code=HTTP_200_OK)
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
