from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.config import APP_CONFIGS, DB_CONFIGS
from app.database import DatabaseManager
from app.users.router import router as users_router

database_manager = DatabaseManager(
    host=DB_CONFIGS["host"],
    port=DB_CONFIGS["port"],
    user=DB_CONFIGS["user"],
    password=DB_CONFIGS["password"],
    database=DB_CONFIGS["database"],
    base=DB_CONFIGS["Base"],
)


@asynccontextmanager
async def lifespan(app):
    logger.info("Starting application")
    await database_manager.connect()
    yield

    logger.info("Stopping application")
    await database_manager.disconnect()


app = FastAPI(
    debug=APP_CONFIGS["debug"],
    title="FastAPI",
    description="Authentication API",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=APP_CONFIGS["allow_origins"],
    allow_credentials=APP_CONFIGS["allow_credentials"],
    allow_methods=APP_CONFIGS["allow_methods"],
    allow_headers=APP_CONFIGS["allow_headers"],
)

app.get(
    "/api/v1/welcome",
    response_model=str,
    response_model_exclude_unset=True,
)(lambda: "Welcome to FastAPI v1")

# Routers
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
