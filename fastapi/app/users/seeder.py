from loguru import logger

from app.exceptions import EntityIntegrityError
from app.users.models import UserCreate
from app.users.repository import UserRepository
from app.users.schema import User


class Seeder(object):
    TABLE_NAME = User.__tablename__
    VALUES = [
        UserCreate(
            username="admin",
            password="admin123",
            email="admin@gmail.com",
            full_name="Admin",
            phone="8700645195",
            role="admin",
            address="Basically heaven, Earth, Milkyway",
        ),
        UserCreate(
            username="customer",
            password="customer123",
            email="customer@gmail.com",
            full_name="Customer",
            phone="8700635185",
            role="customer",
            address="Basically heaven, Cool planet, Andromeda",
        ),
        UserCreate(
            username="seller",
            password="seller123",
            email="seller@gmail.com",
            full_name="Seller",
            phone="8700725185",
            role="seller",
            address="Basically heaven, Cool planet, Cygnus A",
        ),
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
