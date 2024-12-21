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
                    permissions=[],
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
            # Get role and join with permissions
            q = (
                select(Role, Permission.name.label("permission_name"))
                .join(
                    role_permission_association,
                    Role.id == role_permission_association.c.role_id,
                    isouter=True,
                )
                .join(
                    Permission,
                    Permission.id
                    == role_permission_association.c.permission_id,
                    isouter=True,
                )
                .where(Role.id == id)
            )

            result = await connection.execute(q)
            rows = result.fetchall()

            if not rows:
                raise EntityNotFoundError(entity="Role")

            # First row contains the role information
            role = rows[0]

            # Collect all permission names
            permissions = [
                row.permission_name for row in rows if row.permission_name
            ]

            return RoleResponseModel(
                id=role.id,
                name=role.name,
                description=role.description,
                permissions=permissions,
            ).model_dump()

    async def update(self, id: int, role_update: RoleUpdateModel) -> dict:
        async with self.db.engine.begin() as connection:
            try:
                # Check if the role exists
                q = select(Role).where(Role.id == id)
                result = await connection.execute(q)
                if not result.scalar():
                    raise EntityNotFoundError(entity="Role")

                update_values = {}
                if role_update.name is not None:
                    update_values["name"] = role_update.name
                if role_update.description is not None:
                    update_values["description"] = role_update.description

                if role_update.permissions is not None:
                    # Get permission IDs from names
                    q = select(Permission).where(
                        Permission.name.in_(set(role_update.permissions))
                    )
                    result = await connection.execute(q)
                    permissions = result.fetchall()

                    if len(permissions) != len(set(role_update.permissions)):
                        raise EntityNotFoundError(entity="Permission")

                    permission_ids = [p.id for p in permissions]

                    # Delete existing associations
                    q = delete(role_permission_association).where(
                        role_permission_association.c.role_id == id
                    )
                    await connection.execute(q)

                    # Add new associations
                    if permission_ids:
                        values = [
                            {"role_id": id, "permission_id": pid}
                            for pid in permission_ids
                        ]
                        q = insert(role_permission_association).values(values)
                        await connection.execute(q)

                # Update role if there are values to update
                if update_values:
                    q = (
                        update(Role)
                        .where(Role.id == id)
                        .values(**update_values)
                    )
                    await connection.execute(q)

                # Get updated role with permissions
                q = (
                    select(Role, Permission.name.label("permission_name"))
                    .outerjoin(
                        role_permission_association,
                        Role.id == role_permission_association.c.role_id,
                    )
                    .outerjoin(
                        Permission,
                        Permission.id
                        == role_permission_association.c.permission_id,
                    )
                    .where(Role.id == id)
                )
                result = await connection.execute(q)
                rows = result.fetchall()

                if not rows:
                    raise EntityNotFoundError(entity="Role")

                role_data = {
                    "id": rows[0].id,
                    "name": rows[0].name,
                    "description": rows[0].description,
                    "permissions": [
                        row.permission_name
                        for row in rows
                        if row.permission_name
                    ],
                }

                await connection.commit()
                return role_data

            except Exception as e:
                logger.error(f"Error updating role: {e}")
                raise

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
