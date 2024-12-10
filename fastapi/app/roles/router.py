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
)
async def create_role(role: RoleCreateModel):
    try:
        repo = RoleRepository()
        new_role = await repo.create(role)
        return JSONResponse(content=new_role, status_code=HTTP_201_CREATED)
    except EntityIntegrityError as e:
        logger.error(f"Role with name {role.name} already exists")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating role: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/get-all",
    response_model=AllRolesResponseModel,
    status_code=HTTP_200_OK,
)
async def get_all_roles():
    try:
        repo = RoleRepository()
        all_roles = await repo.get_all()
        return JSONResponse(content=all_roles, status_code=HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error getting all roles: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/get-by-id/{id}",
    response_model=RoleResponseModel,
    status_code=HTTP_200_OK,
)
async def get_role_by_id(id: int):
    try:
        repo = RoleRepository()
        role = await repo.get_by_id(id)
        return JSONResponse(content=role, status_code=HTTP_200_OK)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting role by id: {e=}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.put(
    "/update/{id}",
    response_model=RoleResponseModel,
    status_code=HTTP_200_OK,
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