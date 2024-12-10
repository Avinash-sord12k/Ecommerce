from loguru import logger

from app.exceptions import EntityIntegrityError
from app.roles.models import RoleCreateModel
from app.roles.repository import RoleRepository
from app.roles.schema import Role


class Seeder(object):
    TABLE_NAME = Role.__tablename__
    ROLE_VALUES = [
        RoleCreateModel(name="admin", description="Admin of the application"),
        RoleCreateModel(name="customer", description="Buyer of products"),
        RoleCreateModel(name="seller", description="Seller of products"),
    ]
    ROLE_PERMISSION_ASSOCIATION = [
        {"role_id": 1, "permission": "create_role"},
        {"role_id": 1, "permission": "read_role"},
        {"role_id": 1, "permission": "update_role"},
        {"role_id": 1, "permission": "create_permission"},
        {"role_id": 1, "permission": "read_permission"},
        {"role_id": 1, "permission": "create_category"},
        {"role_id": 1, "permission": "read_category"},
        {"role_id": 1, "permission": "delete_category"},
        {"role_id": 1, "permission": "create_subcategory"},
        {"role_id": 1, "permission": "read_subcategory"},
        {"role_id": 1, "permission": "delete_subcategory"},
        {"role_id": 1, "permission": "read_product"},
        {"role_id": 1, "permission": "delete_product"},
        {"role_id": 2, "permission": "read_role"},
        {"role_id": 2, "permission": "read_category"},
        {"role_id": 2, "permission": "read_subcategory"},
        {"role_id": 2, "permission": "read_product"},
        {"role_id": 3, "permission": "read_role"},
        {"role_id": 3, "permission": "read_category"},
        {"role_id": 3, "permission": "read_subcategory"},
        {"role_id": 3, "permission": "read_product"},
        {"role_id": 3, "permission": "create_product"},
        {"role_id": 3, "permission": "update_product"},
        {"role_id": 3, "permission": "delete_product"},
    ]

    @staticmethod
    async def run():
        repo = RoleRepository()
        for value in Seeder.ROLE_VALUES:
            try:
                await repo.create(value)
            except EntityIntegrityError:
                pass
            except Exception as e:
                logger.error(f"Error seeding role: {e=}")

        for value in Seeder.ROLE_PERMISSION_ASSOCIATION:
            try:
                await repo.associate_permission(
                    value["role_id"], value["permission"]
                )
            except EntityIntegrityError:
                pass
            except Exception as e:
                logger.error(f"Error seeding role: {e=}")

        logger.info("Seeding roles completed")
