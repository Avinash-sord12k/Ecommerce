from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidSignatureError,
    InvalidTokenError,
)
from loguru import logger
from sqlalchemy.exc import IntegrityError
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from app.exceptions import EntityIntegrityError
from app.users.models import (
    UserCreate,
    UserLoginLogoutResponse,
    UserRead,
    UserRoles,
)
from app.users.repository import UserRepository
from app.users.utils import (
    create_access_token,
    get_current_user_id,
    token_exists,
)

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.post(
    "/register",
    response_model=UserRead,
    status_code=HTTP_201_CREATED,
)
async def create_user(user: UserCreate):
    try:
        user_repo = UserRepository()
        if user.role not in [UserRoles.CUSTOMER, UserRoles.SELLER]:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Invalid role",
            )
        _user = await user_repo.create(user)
        return UserRead.model_validate(_user)
    except EntityIntegrityError as e:
        logger.error(f"User already exists: {e}")
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="User already exists with this email",
        )
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post("/login", response_model=UserLoginLogoutResponse)
async def login_user(
    request: OAuth2PasswordRequestForm = Depends(), set_cookie: bool = False
):
    try:
        user_repo = UserRepository()
        if not (user := await user_repo.login(request)):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password",
            )

        encode_payload = {"user_id": user.id, "email": user.email}
        token = create_access_token(
            data=encode_payload, expires_delta=timedelta(hours=1)
        )

        # Create response with token in cookie
        response = JSONResponse(
            content={"access_token": token, "token_type": "bearer"}
        )

        if not set_cookie:
            logger.debug(f"Not setting cookie {set_cookie=}")
            return response

        # Set HTTP-only cookie with the token
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=3600,
            path="/",
        )
        response.set_cookie(
            key="token_type",
            value="Bearer",
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=3600,
            path="/",
        )

        return response
    except HTTPException as e:
        logger.exception(f"Error logging in user: {e=}")
        raise e
    except Exception as e:
        logger.error(f"Error logging in user: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/logout", response_model=UserLoginLogoutResponse)
async def logout_user(request: Request):
    try:
        response = JSONResponse(content={"message": "Logged out successfully"})
        response.delete_cookie("access_token")
        return response
    except HTTPException as e:
        logger.exception(f"Error logging out user: {e=}")
        raise e
    except Exception as e:
        logger.error(f"Error logging out user: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get(
    "/me",
    response_model=UserRead,
    dependencies=[Depends(token_exists)],
    openapi_extra={
        "security": [
            {"cookieAuth": [], "oauth2Auth": []},
        ]
    },
)
async def get_user_me(
    user_id: int = Depends(get_current_user_id),
):
    try:
        user_repo = UserRepository()
        logger.info(f"Getting user {user_id=}")
        if not (user := await user_repo.get_by_id(user_id)):
            logger.info(f"{user_id=} not found")
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail="User not found"
            )

        await user_repo.update_last_active(user_id)
        return UserRead.model_validate(user)
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
