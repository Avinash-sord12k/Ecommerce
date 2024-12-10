from datetime import datetime, timezone

from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError

from app.database import DatabaseManager
from app.exceptions import EntityIntegrityError, EntityNotFoundError
from app.roles.schema import Role
from app.users.schema import User
from app.users.utils import hash_password, verify_password


class UserRepository:
    def __init__(self):
        self.db = DatabaseManager._instance

    async def create(self, user: User):
        async with self.db.engine.begin() as connection:
            try:
                q = select(Role).where(Role.name == user.role.value)
                if not (role := (await connection.execute(q)).fetchone()):
                    raise EntityNotFoundError(entity="Role")

                role_id = role[0]
                await connection.execute(
                    insert(User).values(
                        email=user.email,
                        username=user.username,
                        password=hash_password(user.password),
                        full_name=user.full_name,
                        role_id=role_id,
                        phone=user.phone,
                        address=user.address,
                    ),
                )
                result = await connection.execute(
                    select(User).where(User.username == user.username),
                )
                user = result.fetchone()
                await connection.commit()

                logger.info(f"User {user[0]} created successfully")
                return user
            except IntegrityError:
                logger.warning(f"User {user} already exists")
                raise EntityIntegrityError(entity="User")
            except Exception as e:
                logger.error(f"Error creating user: {e=}")
                raise e

    async def update(self, user: User):
        async with self.db.engine.begin() as connection:
            stmt = (
                select(User)
                .where(User.id == id)
                .values(
                    email=user.email,
                    full_name=user.full_name,
                    address=user.address,
                    phone=user.phone,
                    last_active=user.last_active,
                )
            )
            await connection.execute(stmt)
            await connection.commit()
            logger.info(f"User {user.username} updated successfully")

    async def update_last_active(self, user_id: int):
        async with self.db.engine.begin() as connection:
            await connection.execute(
                update(User)
                .where(User.id == user_id)
                .values(last_active=datetime.now(timezone.utc)),
            )
            await connection.commit()
            logger.info(f"User {user_id} updated successfully")

    async def get_by_id(self, user_id: int):
        async with self.db.engine.begin() as connection:
            result = await connection.execute(
                select(User).where(User.id == user_id),
            )
            return result.fetchone()

    async def login(self, user: OAuth2PasswordRequestForm) -> dict:
        async with self.db.engine.begin() as connection:
            stmt = select(User).where(User.username == user.username)
            result = await connection.execute(stmt)

            if not (_user := result.fetchone()):
                logger.error(f"User {user.username} not found")
                return

            if verify_password(user.password, _user.password):
                await connection.commit()
                logger.info(f"User {_user.username} logged in successfully")
                return _user

            await connection.rollback()
            logger.error("Incorrect combination of email and password")
            return _user._asdict()
