import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidSignatureError,
    InvalidTokenError,
)
from loguru import logger
from sqlalchemy.exc import IntegrityError
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from app.config import HASHING_ALGORITHM, SECRET_KEY
from app.users.models import UserCreate, UserLoginResponse, UserRead
from app.users.repository import UserRepository
from app.users.utils import create_access_token

router = APIRouter()

oauth2scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


@router.post("/register", response_model=UserRead)
async def create_user(user: UserCreate):
    try:
        user_repo = UserRepository()
        _user = await user_repo.create(user)
        return UserRead.from_orm(_user)
    except IntegrityError as e:
        logger.error(f"User already exists: {e}")
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User already exists with this email",
        )
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post("/login", response_model=UserLoginResponse)
async def login_user(request: OAuth2PasswordRequestForm = Depends()):
    try:
        user_repo = UserRepository()
        if not (user := await user_repo.login(request)):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password",
            )

        encode_payload = {"user_id": user.id, "email": user.email}
        token = create_access_token(data=encode_payload)
        return UserLoginResponse(access_token=token)
    except HTTPException as e:
        logger.exception(f"Error logging in user: {e=}")
        raise e
    except Exception as e:
        logger.error(f"Error logging in user: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/me", response_model=UserRead)
async def get_user_me(token: str = Depends(oauth2scheme)):
    try:
        token_payload = jwt.decode(
            token, SECRET_KEY, algorithms=[HASHING_ALGORITHM]
        )

        user_repo = UserRepository()
        user_id = token_payload["user_id"]
        if not (user := await user_repo.get_by_id(user_id)):
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail="User not found"
            )

        await user_repo.update_last_active(user_id)
        return UserRead.from_orm(user)
    except InvalidTokenError as e:
        logger.error(f"Invalid token: {e=}")
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    except InvalidSignatureError as e:
        logger.error(f"Invalid signature: {e=}")
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Invalid signature"
        )
    except ExpiredSignatureError as e:
        logger.error(f"Token expired: {e=}")
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except HTTPException as e:
        logger.exception(f"Error getting user: {e=}")
        raise e
    except Exception as e:
        logger.error(f"Error getting user: {e=}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
