from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import ValidationError

from app.config import APP_CONFIGS, DB_CONFIGS
from app.database import DatabaseManager
from app.users.router import router as users_router

database_manager = DatabaseManager(
    host=DB_CONFIGS["host"],
    port=DB_CONFIGS["port"],
    user=DB_CONFIGS["user"],
    password=DB_CONFIGS["password"],
    database=DB_CONFIGS["database"],
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


# Define exception handlers
@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    detail = exc.errors()[0]["msg"] if exc.errors() else "Validation Error"
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content={"detail": detail},
    )


@app.exception_handler(ResponseValidationError)
async def response_validation_exception_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    detail = exc.errors()[0]["msg"] if exc.errors() else "Validation Error"
    logger.error(f"Validation error: {exc.errors(include_url=False)}")
    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content={"detail": detail},
    )


app.get(
    "/api/v1/welcome",
    response_model=str,
    response_model_exclude_unset=True,
    tags=["Default"],
)(lambda: "Welcome to FastAPI v1")

# Routers
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
