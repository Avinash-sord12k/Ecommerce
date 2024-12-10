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
from app.subcategories.models import (
    AllSubCategoriesResponseModel,
    SubCategoryCreateModel,
    SubCategoryResponseModel,
)
from app.subcategories.repository import ProductSubCategoryRepository

router = APIRouter(prefix="/api/v1/subcategory", tags=["SubCategory"])


@router.post(
    "/create",
    response_model=SubCategoryResponseModel,
    status_code=HTTP_201_CREATED,
)
async def create_sub_category(sub_category: SubCategoryCreateModel):
    try:
        repo = ProductSubCategoryRepository()
        new_sub_category = await repo.create(sub_category)
        return SubCategoryResponseModel.model_validate(new_sub_category)
    except EntityIntegrityError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except EntityNotFoundError as e:
        logger.error(f"Category not found: {e=}")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating sub-category: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/get-by-id/{id}",
    response_model=SubCategoryResponseModel,
    status_code=HTTP_200_OK,
)
async def get_sub_category_by_id(id: int):
    try:
        repo = ProductSubCategoryRepository()
        sub_category = await repo.get_by_id(id)
        return JSONResponse(content=sub_category, status_code=HTTP_200_OK)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting sub-category by id: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/get-all",
    response_model=AllSubCategoriesResponseModel,
    status_code=HTTP_200_OK,
)
async def get_sub_category():
    try:
        repo = ProductSubCategoryRepository()
        all_sub_categories = await repo.get_all()
        return JSONResponse(
            content=all_sub_categories.model_dump(),
            status_code=(
                HTTP_200_OK if all_sub_categories else HTTP_404_NOT_FOUND
            ),
        )
    except Exception as e:
        logger.error(f"Error getting sub-categories: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete(
    "/{id}", response_model=SubCategoryResponseModel, status_code=HTTP_200_OK
)
async def delete_sub_category(id: int):
    try:
        logger.info(f"Deleting sub-category with ID: {id}")
        repo = ProductSubCategoryRepository()
        subcategory = await repo.delete(id)
        return JSONResponse(content=subcategory, status_code=HTTP_200_OK)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting sub-category: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)
