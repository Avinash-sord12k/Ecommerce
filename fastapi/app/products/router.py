from fastapi import APIRouter, HTTPException
from loguru import logger
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from app.products.exceptions import (
    CategoryIntegrityError,
    SubCategoryIntegrityError,
)
from app.products.repository import (
    ProductCategoryRepository,
    ProductRepository,
    ProductSubCategoryRepository,
)
from app.products.schema import (
    CategoryCreateSchema,
    CategoryResponseSchema,
    CreateProductRequestSchema,
    ProductResponseSchema,
    SubCategoryCreateSchema,
    SubCategoryResponseSchema,
)

router = APIRouter(prefix="/api/v1/products", tags=["Products"])


@router.post(
    "/create/category",
    response_model=CategoryResponseSchema,
    status_code=HTTP_201_CREATED,
    responses={
        400: {
            "description": "Category with this name already exists.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Category with this name already exists."
                    }
                }
            },
        }
    },
)
async def create_category(category: CategoryCreateSchema):
    try:
        repo = ProductCategoryRepository()
        new_category = await repo.create(category)
        return CategoryResponseSchema.from_orm(new_category)
    except CategoryIntegrityError as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/create/subcategory",
    response_model=SubCategoryResponseSchema,
    status_code=HTTP_201_CREATED,
    responses={
        400: {
            "description": "Sub Category with this name already exists.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Sub Category with this name already exists."
                    }
                }
            },
        }
    },
)
async def create_subcategory(sub_category: SubCategoryCreateSchema):
    try:
        repo = ProductSubCategoryRepository()
        new_sub_category = await repo.create(sub_category)
        return SubCategoryResponseSchema.from_orm(new_sub_category)
    except SubCategoryIntegrityError as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/create",
    response_model=ProductResponseSchema,
    status_code=HTTP_201_CREATED,
)
async def create_product(product: CreateProductRequestSchema):
    try:
        repo = ProductRepository()
        response = await repo.create(product=product)
        return ProductResponseSchema.from_orm(response)
    except Exception as e:
        logger.error(f"Error creating product: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)
