from __future__ import annotations

import os

from sqlalchemy.orm import declarative_base

Base = declarative_base()

SECRET_KEY = "f7559150d081d1ec4e3e5e8e3b77baa3a23a58a52fbdc9b96ffb8110d31b573bcde02a9a2288b4ead72fdc2c79d3cfb9f46e74ebd0ae9ff4c4a55f34490fe1cefb02fb8ac162a5d58e2b14845e2031b94a03f83e9bd5c1bf82b0eb14d652846f23cce9e7"
HASHING_ALGORITHM = "HS256"

APP_CONFIGS = {
    "debug": os.getenv("DEBUG", True),
    "allow_origins": os.getenv("ALLOW_ORIGINS", "*"),
    "allow_credentials": os.getenv("ALLOW_CREDENTIALS", True),
    "allow_methods": os.getenv("ALLOW_METHODS", "*"),
    "allow_headers": os.getenv("ALLOW_HEADERS", "*"),
}

DB_CONFIGS = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", 5432),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "database": os.getenv("DB_DATABASE", "postgres"),
    "pool_size": os.getenv("DB_POOL_SIZE", 20),
}


SHARED_FOLDER = os.getenv("SHARED_FOLDER", "./shared")

TESTMODE = os.getenv("TESTMODE", False)

MAXIMUM_ADDRESS_CREATION_LIMIT_PER_USER = os.getenv(
    "MAXIMUM_ADDRESS_CREATION_LIMIT_PER_USER", 5
)
