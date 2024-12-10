from loguru import logger
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError

from app.database import DatabaseManager
from app.exceptions import EntityIntegrityError, EntityNotFoundError
from app.permissions.schema import Permission, role_permission_association
from app.roles.models import (
    AllRolesResponseModel,
    RoleCreateModel,
    RoleResponseModel,
    RoleUpdateModel,
)
from app.roles.schema import Role


class RoleRepository:
    def __init__(self) -> None:
        self.db = DatabaseManager._instance

    async def create(self, role: RoleCreateModel) -> RoleResponseModel:
        async with self.db.engine.begin() as connection:
            try:
                q = insert(Role).values(
                    name=role.name,
                    description=role.description,
                )
                result = await connection.execute(q)
                await connection.commit()

                return RoleResponseModel(
                    id=result.inserted_primary_key[0],
                    name=role.name,
                    description=role.description,
                    permission_ids=[],
                ).model_dump()
            except IntegrityError:
                logger.error(f"Role with name {role.name} already exists")
                raise EntityIntegrityError(entity="Role")
            except Exception as e:
                logger.error(f"Error creating role: {e=}")
                raise e

    async def get_all(self) -> list[dict]:
        async with self.db.engine.begin() as connection:
            result = await connection.execute(select(Role))
            roles = result.fetchall()
            return AllRolesResponseModel(
                roles=[
                    RoleResponseModel(
                        id=role.id,
                        name=role.name,
                        description=role.description,
                    ).model_dump()
                    for role in roles
                ]
            ).model_dump()

    async def get_by_id(self, id: int) -> RoleResponseModel:
        async with self.db.engine.begin() as connection:
            q = select(Role).where(Role.id == id)
            result = await connection.execute(q)
            role = result.fetchone()
            if not role:
                raise EntityNotFoundError(entity="Role")

            # Get associated permissions
            q = select(role_permission_association).where(
                role_permission_association.c.role_id == role.id
            )
            result = await connection.execute(q)
            associations = result.fetchall()
            return RoleResponseModel(
                id=role.id,
                name=role.name,
                description=role.description,
                permission_ids=[
                    association.permission_id for association in associations
                ],
            ).model_dump()

    async def update(self, id: int, role_update: RoleUpdateModel) -> dict:
        async with self.db.engine.begin() as connection:
            # Check if the role exists
            q = select(Role).where(Role.id == id)
            result = await connection.execute(q)
            if not result.scalar():
                raise EntityNotFoundError(entity="Role")

            # Check if all the permission IDs exist
            q = select(Permission).where(
                Permission.id.in_(role_update.permission_ids)
            )
            result = await connection.execute(q)
            permissions = result.fetchall()
            if len(permissions) != len(role_update.permission_ids):
                raise EntityNotFoundError(entity="Permission")

            # Delete all the existing associations
            q = delete(role_permission_association).where(
                role_permission_association.c.role_id == id
            )
            logger.debug(f"Delete existing associations: {q}")
            await connection.execute(q)

            # Associate the new permissions with the role
            values = [
                {"role_id": id, "permission_id": permission_id}
                for permission_id in role_update.permission_ids
            ]
            logger.debug(f"Insert new associations: {values}")
            q = insert(role_permission_association).values(values)
            await connection.execute(q)

            # update the role
            q = (
                update(Role)
                .where(Role.id == id)
                .values(
                    name=role_update.name,
                    description=role_update.description,
                )
            )
            result = await connection.execute(q)
            await connection.commit()
            return RoleResponseModel(
                id=id,
                name=role_update.name,
                description=role_update.description,
                permission_ids=role_update.permission_ids,
            ).model_dump()
