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

from app.exceptions import (
    EntityIntegrityError,
    EntityNotFoundError,
    NotEnoughPermissionsError,
)
from app.permissions.models import (
    AllPermissionsResponseModel,
    PermissionCreateModel,
    PermissionResponseModel,
)
from app.permissions.repository import PermissionRepository
from app.permissions.utils import check_permissions
from app.users.utils import get_user_id_from_token

router = APIRouter(prefix="/api/v1/permission", tags=["Permission"])


@router.post(
    "/create",
    response_model=PermissionResponseModel,
    status_code=HTTP_201_CREATED,
)
async def create_permission(
    permission: PermissionCreateModel,
    user_id: str = Depends(get_user_id_from_token),
):
    try:
        await check_permissions(user_id, required_roles=["create_permission"])
    except NotEnoughPermissionsError as e:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(e))

    try:
        repo = PermissionRepository()
        new_permission = await repo.create(permission)
        return JSONResponse(
            content=new_permission, status_code=HTTP_201_CREATED
        )
    except EntityIntegrityError as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/get-all",
    response_model=AllPermissionsResponseModel,
    status_code=HTTP_200_OK,
)
async def get_all_permissions(
    user_id: str = Depends(get_user_id_from_token),
):
    try:
        await check_permissions(user_id, required_roles=["read_permission"])
    except NotEnoughPermissionsError as e:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(e))
    try:
        repo = PermissionRepository()
        all_permissions = await repo.get_all()
        return JSONResponse(content=all_permissions, status_code=HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error getting all permissions: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/get-by-id/{id}",
    response_model=PermissionResponseModel,
    status_code=HTTP_200_OK,
)
async def get_permission_by_id(
    id: int,
    user_id: str = Depends(get_user_id_from_token),
):
    try:
        await check_permissions(user_id, required_roles=["read_permission"])
    except NotEnoughPermissionsError as e:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(e))
    try:
        repo = PermissionRepository()
        permission = await repo.get_by_id(id)
        return JSONResponse(content=permission, status_code=HTTP_200_OK)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting permission by id: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)
