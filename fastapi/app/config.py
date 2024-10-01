import os

from sqlalchemy.ext.declarative import declarative_base

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
    "Base": declarative_base(),
}
