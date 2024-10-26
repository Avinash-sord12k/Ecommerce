from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from loguru import logger
from starlette.status import HTTP_401_UNAUTHORIZED

from app.config import HASHING_ALGORITHM, SECRET_KEY

oauth2scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


def hash_password(password):
    hash_bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hash_bytes.decode("utf-8")


def verify_password(password: str, hash: str):
    return bcrypt.checkpw(password.encode("utf-8"), hash.encode("utf-8"))


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expires_delta = expires_delta or timedelta(minutes=15)
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    encoded_jwt = jwt.encode(
        payload=to_encode, key=SECRET_KEY, algorithm=HASHING_ALGORITHM
    )
    return encoded_jwt


def get_user_id_from_token(token: str = Depends(oauth2scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASHING_ALGORITHM])
        if user_id := payload["user_id"]:
            return user_id

        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    except jwt.ExpiredSignatureError as e:
        logger.error(f"Token expired: {e=}")
        return None
    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid token: {e=}")
        return None
    except jwt.InvalidSignatureError as e:
        logger.error(f"Invalid signature: {e=}")
        return None
    except Exception as e:
        logger.error(f"Error getting user id from token: {e=}")
