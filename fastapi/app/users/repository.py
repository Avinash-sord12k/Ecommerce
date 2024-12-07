from datetime import datetime

from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from sqlalchemy import insert, select, update

from app.database import DatabaseManager
from app.users.models import User
from app.users.utils import hash_password, verify_password


class UserRepository:
    def __init__(self):
        self.db = DatabaseManager._instance

    async def create(self, user: User):
        async with self.db.engine.begin() as connection:
            await connection.execute(
                insert(User).values(
                    email=user.email,
                    username=user.username,
                    password=hash_password(user.password),
                    full_name=user.full_name,
                    address=user.address,
                    phone=user.phone,
                ),
            )
            result = await connection.execute(
                select(User).where(User.username == user.username),
            )
            user = result.fetchone()
            await connection.commit()
            logger.info(f"User {user[0]} created successfully")
        return user

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
            await connection.execute(update(User).where(User.id == user_id).values(last_active=datetime.now()))
            await connection.commit()
            logger.info(f"User {user_id} updated successfully")

    async def get_by_id(self, user_id: int):
        async with self.db.engine.begin() as connection:
            result = await connection.execute(
                select(User).where(User.id == user_id),
            )
            return result.fetchone()

    async def login(self, user: OAuth2PasswordRequestForm):
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
            return
