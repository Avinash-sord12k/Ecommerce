from venv import logger
from fastapi import APIRouter, Depends, HTTPException
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)

from app.address.exceptions import MaximumAddressLimitReachedError
from app.address.repository import AddressRepository
from app.address.models import (
    AddressResponseModel,
    AddressCreateModel,
    AllAddressResponseModel,
)
from app.exceptions import EntityNotFoundError
from app.permissions.utils import allowed_permissions
from app.users.utils import get_user_id_from_token


router = APIRouter(prefix="/api/v1/address", tags=["Address"])


@router.post(
    "/create",
    response_model=AddressResponseModel,
    status_code=HTTP_201_CREATED,
    dependencies=[
        Depends(allowed_permissions(["create_address"])),
    ],
)
async def create_address(
    address: AddressCreateModel, user_id: int = Depends(get_user_id_from_token)
):
    try:
        repo = AddressRepository()
        address_id = await repo.create(1, address)
        address = await repo.get(user_id=user_id, address_id=address_id)
        return AddressResponseModel(**address)
    except MaximumAddressLimitReachedError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.exception(f"While creating addresss: {e}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/get-by-id/{id}",
    response_model=AddressResponseModel,
    status_code=HTTP_200_OK,
    dependencies=[
        Depends(allowed_permissions(["read_address"])),
    ],
)
async def get_address(id: int, user_id: int = Depends(get_user_id_from_token)):
    try:
        repo = AddressRepository()
        address = await repo.get(user_id=user_id, address_id=id)
        return AddressResponseModel(**address)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.exception(f"While reading address {e}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/get-all",
    response_model=AllAddressResponseModel,
    status_code=HTTP_200_OK,
    dependencies=[
        Depends(allowed_permissions(["read_address"])),
    ],
)
async def get_all_address(
    id: int, user_id: int = Depends(get_user_id_from_token)
):
    try:
        repo = AddressRepository()
        addresses = await repo.get_all(user_id=user_id)
        return AllAddressResponseModel(
            addresses=[
                AddressResponseModel(**address) for address in addresses
            ]
        )
    except Exception as e:
        logger.exception(f"While reading all addresses: {e}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))


@router.put(
    "/update/{id}",
    response_model=AddressResponseModel,
    status_code=HTTP_200_OK,
    dependencies=[
        Depends(allowed_permissions(["update_address"])),
    ],
)
async def update_address(
    id: int,
    address: AddressCreateModel,
    user_id: int = Depends(get_user_id_from_token),
):
    try:
        repo = AddressRepository()
        address_id = await repo.update(
            user_id=user_id, address_id=id, address=address
        )
        address = await repo.get(user_id=user_id, address_id=address_id)
        return AddressResponseModel(**address)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.exception(f"While updating address: {e}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{id}",
    response_model=AddressResponseModel,
    status_code=HTTP_200_OK,
    dependencies=[
        Depends(allowed_permissions(["delete_address"])),
    ],
)
async def delete_address(
    id: int, user_id: int = Depends(get_user_id_from_token)
):
    try:
        repo = AddressRepository()
        address_id = await repo.delete(user_id=user_id, address_id=id)
        address = await repo.get(user_id=user_id, address_id=address_id)
        return AddressResponseModel(**address)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.exception(f"While deleting address: {e}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))