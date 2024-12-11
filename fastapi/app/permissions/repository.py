from loguru import logger
from sqlalchemy import insert, select, delete
from sqlalchemy.exc import IntegrityError

from app.database import DatabaseManager
from app.exceptions import EntityIntegrityError, EntityNotFoundError
from app.permissions.models import (
    PermissionCreateModel,
    PermissionResponseModel,
)
from app.permissions.schema import Permission


class PermissionRepository:
    def __init__(self) -> None:
        self.db = DatabaseManager._instance

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

    async def get_all(self) -> list[dict]:
        async with self.db.engine.begin() as connection:
            result = await connection.execute(select(Permission))
            permissions = result.fetchall()
            return [
                PermissionResponseModel(
                    id=permission.id,
                    name=permission.name,
                    description=permission.description,
                ).model_dump()
                for permission in permissions
            ]

    async def get_by_id(self, id: int) -> PermissionResponseModel:
        async with self.db.engine.begin() as connection:
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
