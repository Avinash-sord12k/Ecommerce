from typing import List, Optional

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
from app.models import PaginationParams
from app.permissions.utils import allowed_permissions
from app.roles.models import (
    AllRolesResponseModel,
    RoleCreateModel,
    RoleResponseModel,
    RoleUpdateModel,
)
from app.roles.repository import RoleRepository

router = APIRouter(prefix="/api/v1/role", tags=["Role"])


@router.post(
    "/create",
    response_model=RoleResponseModel,
    status_code=HTTP_201_CREATED,
    dependencies=[
        Depends(allowed_permissions(["create_role"])),
    ],
    description="Create a new role with no initial permissions",
    openapi_extra={
        "security": [
            {"cookieAuth": [], "oauth2Auth": []},
        ]
    },
)
async def create_role(role: RoleCreateModel):
    try:
        repo = RoleRepository()
        new_role = await repo.create(role)
        return JSONResponse(content=new_role, status_code=HTTP_201_CREATED)
    except EntityIntegrityError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating role: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "",
    response_model=AllRolesResponseModel,
    status_code=HTTP_200_OK,
    dependencies=[
        Depends(allowed_permissions(["read_role"])),
    ],
    description="Get all roles with pagination and optional role ID filter",
    openapi_extra={
        "security": [
            {"cookieAuth": [], "oauth2Auth": []},
        ]
    },
)
async def get_all_roles(
    role_id: int = None,
    include_permissions: bool = False,
    pagination: PaginationParams = Depends(),
):
    try:
        repo = RoleRepository()
        all_roles = await repo.get_all(
            page=pagination.page,
            page_size=pagination.page_size,
            role_id=role_id,
            include_permissions=include_permissions,
        )
        return JSONResponse(content=all_roles, status_code=HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error getting all roles: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.put(
    "/update/{id}",
    response_model=RoleResponseModel,
    status_code=HTTP_200_OK,
    dependencies=[
        Depends(allowed_permissions(["update_role"])),
    ],
    description="Update a role's information and permissions",
    openapi_extra={
        "security": [
            {"cookieAuth": [], "oauth2Auth": []},
        ]
    },
)
async def update_role(id: int, role: RoleUpdateModel):
    try:
        repo = RoleRepository()
        role = await repo.update(id, role)
        return JSONResponse(content=role, status_code=HTTP_200_OK)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating role: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete(
    "/{id}",
    status_code=HTTP_200_OK,
    dependencies=[
        Depends(allowed_permissions(["delete_role"])),
    ],
    description="Delete a role and its permission associations",
    openapi_extra={
        "security": [
            {"cookieAuth": [], "oauth2Auth": []},
        ]
    },
)
async def delete_role(id: int):
    try:
        repo = RoleRepository()
        await repo.delete(id)
        return JSONResponse(content={}, status_code=HTTP_200_OK)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except NotEnoughPermissionsError as e:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting role: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)
