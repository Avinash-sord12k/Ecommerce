import os
from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import ValidationError

from app.address.router import router as address_router
from app.cart.router import router as cart_router
from app.categories.router import router as category_router
from app.config import APP_CONFIGS, SHARED_FOLDER
from app.database import DatabaseManager
from app.permissions.router import router as permissions_router
from app.permissions.seeder import Seeder as PermissionSeeder
from app.products.router import router as products_router
from app.roles.router import router as roles_router
from app.roles.seeder import Seeder as RoleSeeder
from app.subcategories.router import router as subcategory_router
from app.users.router import router as users_router
from app.users.seeder import Seeder as UserSeeder
from app.products.seeder import Seeder as ProductSeeder
from app.categories.seeder import Seeder as CategorySeeder


@asynccontextmanager
async def lifespan(app):
    logger.info("Starting application")

    database_manager = DatabaseManager()
    await database_manager.connect()

    logger.info("Seeding database")
    await PermissionSeeder().run()
    await RoleSeeder().run()
    await UserSeeder().run()
    await ProductSeeder().run()
    await CategorySeeder().run()

    os.makedirs(SHARED_FOLDER, exist_ok=True)
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
    tags=["Default"],
)(lambda: "Welcome to FastAPI v1")


# Routers
app.include_router(router=users_router)
app.include_router(router=address_router)
app.include_router(router=roles_router)
app.include_router(router=permissions_router)
app.include_router(router=category_router)
app.include_router(router=subcategory_router)
app.include_router(router=products_router)
app.include_router(router=cart_router)


# Define exception handlers
@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    detail = exc.errors()[0]["msg"] if exc.errors() else "Validation Error"
    logger.error(f"Validation error: {exc.errors()}")
    raise HTTPException(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=detail
    )


@app.exception_handler(ResponseValidationError)
async def response_validation_exception_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    detail = exc.errors()[0]["msg"] if exc.errors() else "Validation Error"
    logger.error(f"Validation error: {exc.errors()}")
    raise HTTPException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=detail
    )
