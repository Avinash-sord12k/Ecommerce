from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from app.categories.models import (
    AllCategoriesResponseModel,
    CategoryCreateModel,
    CategoryResponseModel,
)
from app.categories.repository import ProductCategoryRepository
from app.exceptions import (
    EntityIntegrityError,
    EntityNotFoundError,
    NotEnoughPermissionsError,
)
from app.permissions.utils import check_permissions
from app.users.utils import get_user_id_from_token

router = APIRouter(prefix="/api/v1/category", tags=["Category"])


@router.post(
    "/create",
    response_model=CategoryResponseModel,
    status_code=HTTP_201_CREATED,
)
async def create_category(
    category: CategoryCreateModel,
    user_id: str = Depends(get_user_id_from_token),
):
    try:
        await check_permissions(user_id, required_roles=["create_category"])
    except NotEnoughPermissionsError as e:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(e))

    try:
        repo = ProductCategoryRepository()
        new_category = await repo.create(category)
        return CategoryResponseModel.model_validate(new_category)
    except EntityIntegrityError as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/get-by-id/{id}",
    response_model=CategoryResponseModel,
    status_code=HTTP_200_OK,
)
async def get_category_by_id(
    id: int,
    user_id: str = Depends(get_user_id_from_token),
):
    try:
        await check_permissions(user_id, required_roles=["read_category"])
    except NotEnoughPermissionsError as e:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(e))

    try:
        repo = ProductCategoryRepository()
        category = await repo.get_by_id(id)
        return JSONResponse(content=category, status_code=HTTP_200_OK)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting category by id: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/get-all",
    response_model=AllCategoriesResponseModel,
    status_code=HTTP_200_OK,
)
async def get_category(
    user_id: str = Depends(get_user_id_from_token),
):
    try:
        await check_permissions(user_id, required_roles=["read_category"])
    except NotEnoughPermissionsError as e:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(e))

    try:
        repo = ProductCategoryRepository()
        all_categories = await repo.get_all()
        return JSONResponse(
            content=all_categories.model_dump(),
            status_code=(
                HTTP_200_OK if all_categories else HTTP_404_NOT_FOUND
            ),
        )
    except Exception as e:
        logger.error(f"Error getting categories: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete(
    "/{id}", response_model=CategoryResponseModel, status_code=HTTP_200_OK
)
async def delete_category(
    id: int,
    user_id: str = Depends(get_user_id_from_token),
):
    try:
        await check_permissions(user_id, required_roles=["delete_category"])
    except NotEnoughPermissionsError as e:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(e))

    if not isinstance(id, int):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid ID"
        )

    try:
        repo = ProductCategoryRepository()
        category = await repo.delete(id)
        return JSONResponse(content=category, status_code=HTTP_200_OK)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting category: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)
