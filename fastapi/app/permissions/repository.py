from loguru import logger
from sqlalchemy import delete, func, insert, select
from sqlalchemy.exc import IntegrityError

from app.database import DatabaseManager
from app.exceptions import EntityIntegrityError, EntityNotFoundError
from app.permissions.models import (
    PermissionCreateModel,
    PermissionResponseModel,
)
from app.permissions.schema import Permission
from app.repository import BaseRepository


class PermissionRepository(BaseRepository):
    def __init__(self) -> None:
        self.db = DatabaseManager._instance
        super().__init__(self.db)

    async def create(
        self, permission: PermissionCreateModel
    ) -> PermissionResponseModel:
        async with self.db.engine.begin() as connection:
            try:
                q = insert(Permission).values(
                    name=permission.name,
                    description=permission.description,
                )
                result = await connection.execute(q)
                await connection.commit()

                return PermissionResponseModel(
                    id=result.inserted_primary_key[0],
                    name=permission.name,
                    description=permission.description,
                ).model_dump()
            except IntegrityError:
                logger.warning(f"Permission {permission.name} already exists")
                raise EntityIntegrityError(entity="Permission")
            except Exception as e:
                logger.error(f"Error creating permission: {e=}")
                raise e

    async def get_all(
        self,
        permission_id: int | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict], int]:
        query = select(Permission)
        if permission_id is not None:
            query = query.where(Permission.id == permission_id)
            async with self.db.engine.begin() as connection:
                result = await connection.execute(query)
                if not result.fetchone():
                    raise EntityNotFoundError(entity="Permission")

        items, total = await self.get_paginated(query, page, page_size)

        return [
            PermissionResponseModel(
                id=item["id"],
                name=item["name"],
                description=item["description"],
            ).model_dump()
            for item in items
        ], total

    async def get(self, id: int = None) -> PermissionResponseModel:
        async with self.db.engine.begin() as connection:
            if id is None:
                q = select(Permission).order_by(func.random()).limit(1)
            else:
                q = select(Permission).where(Permission.id == id)

            result = await connection.execute(q)
            permission = result.fetchone()
            if not permission:
                raise EntityNotFoundError(entity="Permission")

            return permission._asdict()

    async def delete(self, id: int):
        async with self.db.engine.begin() as connection:
            try:
                q = select(Permission).where(Permission.id == id)
                result = await connection.execute(q)
                if not result.fetchone():
                    raise EntityNotFoundError(entity="Permission")

                q = delete(Permission).where(Permission.id == id)
                await connection.execute(q)
                await connection.commit()
                return True
            except EntityNotFoundError as e:
                logger.error(f"Error deleting permission: {e=}")
                raise e
            except Exception as e:
                logger.error(f"Error deleting permission: {e=}")
                raise e
