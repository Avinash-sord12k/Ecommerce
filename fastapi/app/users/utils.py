from datetime import datetime, timedelta

import bcrypt
import jwt

from app.config import HASHING_ALGORITHM, SECRET_KEY


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
