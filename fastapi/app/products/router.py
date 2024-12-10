from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from app.exceptions import EntityIntegrityError, EntityNotFoundError
from app.products.models import (
    CreateProductRequestModel,
    ProductResponseModel,
    UpdateProductRequestModel,
)
from app.products.repository import ProductRepository

router = APIRouter(prefix="/api/v1/product", tags=["Product"])


@router.post(
    "/create",
    response_model=ProductResponseModel,
    status_code=HTTP_201_CREATED,
)
async def create_product(product: CreateProductRequestModel):
    try:
        repo = ProductRepository()
        new_product_id = await repo.create(product)
        return ProductResponseModel(id=new_product_id, **product.model_dump())
    except EntityNotFoundError as e:
        logger.error(f"Some dependency not found: {e=}")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except EntityIntegrityError as e:
        logger.error(f"Product or Dependency already exists: {e=}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating product: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/get-by-id/{id}",
    response_model=ProductResponseModel,
    status_code=HTTP_200_OK,
)
async def get_product_by_id(id: int):
    try:
        repo = ProductRepository()
        product = await repo.get_by_id(id)
        return JSONResponse(content=product, status_code=HTTP_200_OK)
    except EntityNotFoundError as e:
        logger.error(f"Product not found: {e=}")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting product by id: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/get-by-category-id/{category_id}",
    response_model=ProductResponseModel,
    status_code=HTTP_200_OK,
)
async def get_product_by_category_id(category_id: int):
    try:
        repo = ProductRepository()
        products = await repo.get_by_category_id(category_id)
        return JSONResponse(content=products, status_code=HTTP_200_OK)
    except EntityNotFoundError as e:
        logger.error(f"Category not found: {e=}")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting products by category: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/get-by-subcategory-id/{sub_category_id}",
    response_model=ProductResponseModel,
    status_code=HTTP_200_OK,
)
async def get_product_by_sub_category_id(sub_category_id: int):
    try:
        repo = ProductRepository()
        products = await repo.get_by_subcategory_id(sub_category_id)
        return JSONResponse(content=products, status_code=HTTP_200_OK)
    except EntityNotFoundError as e:
        logger.error(f"Sub-category not found: {e=}")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting products by sub-category id: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.put(
    "/update/{id}",
    response_model=ProductResponseModel,
    status_code=HTTP_200_OK,
)
async def update_product(id: int, product: UpdateProductRequestModel):
    try:
        repo = ProductRepository()
        product = await repo.update(id, product)
        return JSONResponse(content=product, status_code=HTTP_200_OK)
    except EntityNotFoundError as e:
        logger.error(f"Product not found: {e=}")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating product: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete(
    "/{id}", response_model=ProductResponseModel, status_code=HTTP_200_OK
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
