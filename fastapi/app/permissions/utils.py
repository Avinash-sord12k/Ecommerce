from loguru import logger
from sqlalchemy import select

from app.exceptions import EntityNotFoundError, NotEnoughPermissionsError
from app.database import DatabaseManager
from app.users.schema import User


async def check_permissions(user_id: str, required_roles: list[str]):
    db_instance = DatabaseManager()._instance
    async with db_instance.engine.begin() as connection:
        q = select(User).where(User.id == user_id)
        result = await connection.execute(q)

        if not (user := result.fetchone()):
            raise EntityNotFoundError(entity="User")

        user_asdict = user._asdict()
        if user_asdict["role"] not in required_roles:
            logger.error("User does not have enough permissions")
            raise NotEnoughPermissionsError(message="Missing permissions")

        return user
