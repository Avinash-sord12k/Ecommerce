from __future__ import annotations

from app.users.models import UserCreate
from app.users.repository import UserRepository
from loguru import logger
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from fastapi import APIRouter
from fastapi import HTTPException

router = APIRouter()


@router.post("/users", response_model=UserCreate)
async def create_user(user: UserCreate):
    try:
        user_repo = UserRepository()
        await user_repo.create(user)

        return user
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/users/{user_id}", response_model=UserCreate)
async def get_user_by_id(user_id: int):
    user_repo = UserRepository()
    user = await user_repo.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/{username}", response_model=UserCreate)
async def get_user_by_username(username: str):
    user_repo = UserRepository()
    user = await user_repo.get_by_username(username)
    if user is None:
        raise HTTPException
