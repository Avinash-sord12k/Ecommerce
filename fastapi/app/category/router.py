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

from app.category.repository import ProductCategoryRepository
from app.category.schema import CategoryCreateSchema, CategoryResponseSchema
from app.exceptions import EntityIntegrityError, EntityNotFoundError

router = APIRouter(prefix="/api/v1/category", tags=["Category"])


@router.post(
    "/create",
    response_model=CategoryResponseSchema,
    status_code=HTTP_201_CREATED,
    responses={
        400: {
            "description": "Category with this name already exists.",
            "content": {"application/json": {"example": {"detail": "Category with this name already exists."}}},
        }
    },
)
async def create_category(category: CategoryCreateSchema):
    try:
        repo = ProductCategoryRepository()
        new_category = await repo.create(category)
        return CategoryResponseSchema.model_validate(new_category)
    except EntityIntegrityError as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/get_by_id/{id}", response_model=CategoryResponseSchema, status_code=HTTP_200_OK)
async def get_category_by_id(id: int):
    try:
        repo = ProductCategoryRepository()
        category = await repo.get_by_id(id)
        return JSONResponse(content=category, status_code=HTTP_200_OK)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting category by id: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/delete/{id}", response_model=CategoryResponseSchema, status_code=HTTP_200_OK)
async def delete_category(id: int):
    if not isinstance(id, int):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid ID")

    try:
        repo = ProductCategoryRepository()
        category = await repo.delete(id)
        return JSONResponse(content=category, status_code=HTTP_200_OK)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting category: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)
