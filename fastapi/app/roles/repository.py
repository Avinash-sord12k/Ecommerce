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
                logger.warning(f"Role {role.name} already exists")
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

    async def associate_permission(self, role: int, permission: str):
        async with self.db.engine.begin() as connection:
            try:
                # Get the role id from role name
                q = select(Role).where(Role.name == role)
                result = (await connection.execute(q)).fetchone()
                if not result:
                    raise EntityNotFoundError(entity="Role")

                role_id = result[0]

                # Get permission id from permission name
                q = select(Permission).where(Permission.name == permission)
                result = await connection.execute(q)
                permission_id = result.fetchone()[0]
            except EntityNotFoundError as e:
                logger.error(f"Error fetching role or permission: {e=}")
                raise e
            except Exception as e:
                logger.error(f"Error fetching role or permission: {e=}")
                raise e

            try:
                # Associate the permission with the role
                q = insert(role_permission_association).values(
                    role_id=role_id, permission_id=permission_id
                )
                await connection.execute(q)
                await connection.commit()
                return True
            except IntegrityError:
                logger.warning(
                    "Role Permission association "
                    + f"{role_id} {permission_id} already exists"
                )
                raise EntityIntegrityError(entity="Permission")
            except Exception as e:
                logger.error(
                    f"Error creating role permission association: {e=}"
                )
                raise e

    async def delete(self, id: int):
        async with self.db.engine.begin() as connection:
            try:
                q = select(Role).where(Role.id == id)
                result = await connection.execute(q)
                if not result.scalar():
                    raise EntityNotFoundError(entity="Role")

                q = delete(Role).where(Role.id == id)
                await connection.execute(q)
                await connection.commit()
                return True
            except EntityNotFoundError as e:
                logger.error(f"Error deleting role: {e=}")
                raise e
            except Exception as e:
                logger.error(f"Error deleting role: {e=}")
                raise e
