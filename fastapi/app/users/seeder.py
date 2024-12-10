from loguru import logger

from app.exceptions import EntityIntegrityError
from app.users.models import UserCreate
from app.users.repository import UserRepository
from app.users.schema import User


class Seeder(object):
    TABLE_NAME = User.__tablename__
    VALUES = [
        UserCreate(
            username="ashishk2004a",
            password="dummypassword123",
            email="ashishk2004a@gmail.com",
            full_name="Ashish Kumar Jha",
            phone="8700745195",
            role="admin",
            address="Basically heaven, Earth, Milkyway",
        )
    ]

    @staticmethod
    async def run():
        repo = UserRepository()
        for value in Seeder.VALUES:
            try:
                await repo.create(value)
            except EntityIntegrityError:
                pass
            except Exception as e:
                logger.error(f"Error seeding user: {e=}")

        logger.info("Seeding users completed")
