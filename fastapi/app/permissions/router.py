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
from app.models import PaginationParams
from app.permissions.models import (
    AllPermissionsResponseModel,
    PermissionCreateModel,
    PermissionResponseModel,
)
from app.permissions.repository import PermissionRepository
from app.permissions.utils import allowed_permissions

router = APIRouter(prefix="/api/v1/permission", tags=["Permission"])


@router.post(
    "/create",
    response_model=PermissionResponseModel,
    status_code=HTTP_201_CREATED,
    dependencies=[
        Depends(allowed_permissions(["create_permission"])),
    ],
    openapi_extra={
        "security": [
            {"cookieAuth": [], "oauth2Auth": []},
        ]
    },
)
async def create_permission(permission: PermissionCreateModel):
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
    "",
    response_model=AllPermissionsResponseModel,
    status_code=HTTP_200_OK,
    dependencies=[
        Depends(allowed_permissions(["read_permission"])),
    ],
    openapi_extra={
        "security": [
            {"cookieAuth": [], "oauth2Auth": []},
        ]
    },
)
async def get_all_permissions(
    permission_id: int | None = None, pagination: PaginationParams = Depends()
):
    try:
        repo = PermissionRepository()
        permissions, total = await repo.get_all(
            permission_id=permission_id,
            page=pagination.page,
            page_size=pagination.page_size,
        )

        response = {
            "items": permissions,
            "total": total,
            "page": pagination.page,
            "page_size": pagination.page_size,
            "total_pages": (total + pagination.page_size - 1)
            // pagination.page_size,
        }

        return JSONResponse(content=response, status_code=HTTP_200_OK)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting all permissions: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete(
    "/{id}",
    status_code=HTTP_200_OK,
    dependencies=[
        Depends(allowed_permissions(["delete_permission"])),
    ],
    openapi_extra={
        "security": [
            {"cookieAuth": [], "oauth2Auth": []},
        ]
    },
)
async def delete_permission(id: int):
    try:
        repo = PermissionRepository()
        await repo.delete(id)
        return JSONResponse(content={}, status_code=HTTP_200_OK)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting permission: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)
