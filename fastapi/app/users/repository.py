from __future__ import annotations

from sqlalchemy import select

from app.database import DatabaseManager
from app.users.models import User


class UserRepository:
    def __init__(self):
        self.db = DatabaseManager._instance

    async def create(self, user: User):
        async with self.db.pool.acquire() as connection:
            await connection.execute(
                User.__table__.insert(),
                {
                    "username": user.username,
                    "email": user.email,
                    "password": user.password,
                    "full_name": user.full_name,
                    "phone": user.phone,
                    "address": user.address,
                },
            )
            await connection.commit()

    async def get_by_id(self, user_id: int):
        async with self.db.pool.acquire() as connection:
            result = await connection.fetch(
                select(User).where(User.id == user_id),
            )
            return result[0]

    async def get_by_username(self, username: str):
        async with self.db.pool.acquire() as connection:
            result = await connection.fetch(
                select(User).where(User.username == username),
            )
            return result[0]
