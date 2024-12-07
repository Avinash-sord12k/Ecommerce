from fastapi import APIRouter, HTTPException
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
from app.subcategory.repository import ProductSubCategoryRepository
from app.subcategory.schema import (
    AllSubCategoriesResponseSchema,
    SubCategoryCreateSchema,
    SubCategoryResponseSchema,
)

router = APIRouter(prefix="/api/v1/subcategory", tags=["SubCategory"])


@router.post(
    "/create",
    response_model=SubCategoryResponseSchema,
    status_code=HTTP_201_CREATED,
    responses={
        400: {
            "description": "Sub-category with this name already exists.",
            "content": {"application/json": {"example": {"detail": "Sub-category with this name already exists."}}},
        }
    },
)
async def create_sub_category(sub_category: SubCategoryCreateSchema):
    try:
        repo = ProductSubCategoryRepository()
        new_sub_category = await repo.create(sub_category)
        return SubCategoryResponseSchema.model_validate(new_sub_category)
    except EntityIntegrityError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/get-all",
    response_model=AllSubCategoriesResponseSchema,
    status_code=HTTP_200_OK,
    responses={
        404: {
            "description": "No sub-categories found.",
            "content": {"application/json": {"example": {"detail": "No sub-categories found."}}},
        },
        500: {
            "description": "Internal server error.",
            "content": {"application/json": {"example": {"detail": "Internal server error."}}},
        },
    },
)
async def get_sub_category():
    try:
        repo = ProductSubCategoryRepository()
        all_sub_categories = await repo.get_all()
        return JSONResponse(
            content=all_sub_categories.model_dump(),
            status_code=(HTTP_200_OK if all_sub_categories else HTTP_404_NOT_FOUND),
        )
    except Exception as e:
        logger.error(f"Error getting sub-categories: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{name}", status_code=HTTP_200_OK)
async def delete_sub_category(name: str):
    try:
        repo = ProductSubCategoryRepository()
        await repo.delete(name)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting sub-category: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)
