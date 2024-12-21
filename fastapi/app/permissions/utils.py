from functools import wraps

from fastapi import Depends, HTTPException
from loguru import logger
from sqlalchemy import select
from starlette.status import HTTP_403_FORBIDDEN

from app.database import DatabaseManager
from app.exceptions import EntityNotFoundError, NotEnoughPermissionsError
from app.permissions.schema import Permission, role_permission_association
from app.users.schema import User
from app.users.utils import get_current_user_id


def allowed_permissions(required_permissions: list):
    async def permission_checker(
        user_id: int = Depends(get_current_user_id),
    ):
        try:
            db_instance = DatabaseManager._instance
            async with db_instance.engine.begin() as connection:

                # Get User's Role ID
                q = select(User).where(User.id == user_id)
                result = await connection.execute(q)

                if not (user := result.fetchone()):
                    raise EntityNotFoundError(entity="User")

                user_asdict = user._asdict()
                role_id = user_asdict["role_id"]

                associations_to_check = []

                # Get ID of all required permissions and populate associations to check
                for permission in required_permissions:
                    q = select(Permission).where(Permission.name == permission)
                    result = await connection.execute(q)
                    permission_asdict = result.fetchone()._asdict()
                    associations_to_check.append(
                        {
                            "role_id": role_id,
                            "permission_id": permission_asdict["id"],
                        }
                    )

                # Check if all the associations exists
                q = select(role_permission_association).where(
                    role_permission_association.c.role_id.in_(
                        [
                            association["role_id"]
                            for association in associations_to_check
                        ]
                    ),
                    role_permission_association.c.permission_id.in_(
                        [
                            association["permission_id"]
                            for association in associations_to_check
                        ]
                    ),
                )
                result = await connection.execute(q)
                associations = result.fetchall()
                if len(associations) != len(required_permissions):
                    logger.error("User does not have enough permissions")
                    raise NotEnoughPermissionsError(
                        message="Missing permissions"
                    )

                return user
        except NotEnoughPermissionsError as e:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(e))

    return permission_checker
