from loguru import logger

from app.exceptions import EntityIntegrityError
from app.roles.models import RoleCreateModel
from app.roles.repository import RoleRepository
from app.roles.schema import Role


class Seeder(object):
    TABLE_NAME = Role.__tablename__
    VALUES = [
        RoleCreateModel(name="admin", description="Admin of the application"),
        RoleCreateModel(name="customer", description="Buyer of products"),
        RoleCreateModel(name="seller", description="Seller of products"),
    ]

    @staticmethod
    async def run():
        repo = RoleRepository()
        for value in Seeder.VALUES:
            try:
                await repo.create(value)
            except EntityIntegrityError as e:
                logger.warning(f"Role already exists {e=}")
            except Exception as e:
                logger.error(f"Error seeding role: {e=}")
