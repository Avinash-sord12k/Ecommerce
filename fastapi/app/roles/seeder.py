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
        RoleCreateModel(name="tester", description="Tester of application"),
    ]
    ROLE_PERMISSION_ASSOCIATION = [
        {"role": "admin", "permission": "create_role"},
        {"role": "admin", "permission": "read_role"},
        {"role": "admin", "permission": "update_role"},
        {"role": "admin", "permission": "create_permission"},
        {"role": "admin", "permission": "read_permission"},
        {"role": "admin", "permission": "create_category"},
        {"role": "admin", "permission": "read_category"},
        {"role": "admin", "permission": "delete_category"},
        {"role": "admin", "permission": "create_subcategory"},
        {"role": "admin", "permission": "read_subcategory"},
        {"role": "admin", "permission": "delete_subcategory"},
        {"role": "admin", "permission": "read_product"},
        {"role": "admin", "permission": "delete_product"},
        {"role": "customer", "permission": "read_role"},
        {"role": "customer", "permission": "read_category"},
        {"role": "customer", "permission": "read_subcategory"},
        {"role": "customer", "permission": "read_product"},
        {"role": "customer", "permission": "create_cart"},
        {"role": "customer", "permission": "read_cart"},
        {"role": "customer", "permission": "update_cart"},
        {"role": "customer", "permission": "delete_cart"},
        {"role": "seller", "permission": "read_role"},
        {"role": "seller", "permission": "read_category"},
        {"role": "seller", "permission": "read_subcategory"},
        {"role": "seller", "permission": "read_product"},
        {"role": "seller", "permission": "create_product"},
        {"role": "seller", "permission": "update_product"},
        {"role": "seller", "permission": "delete_product"},
        {"role": "tester", "permission": "create_role"},
        {"role": "tester", "permission": "read_role"},
        {"role": "tester", "permission": "update_role"},
        {"role": "tester", "permission": "delete_role"},
        {"role": "tester", "permission": "create_permission"},
        {"role": "tester", "permission": "read_permission"},
        {"role": "tester", "permission": "delete_permission"},
        {"role": "tester", "permission": "create_category"},
        {"role": "tester", "permission": "read_category"},
        {"role": "tester", "permission": "delete_category"},
        {"role": "tester", "permission": "create_subcategory"},
        {"role": "tester", "permission": "read_subcategory"},
        {"role": "tester", "permission": "delete_subcategory"},
        {"role": "tester", "permission": "read_product"},
        {"role": "tester", "permission": "delete_product"},
        {"role": "tester", "permission": "create_cart"},
        {"role": "tester", "permission": "read_cart"},
        {"role": "tester", "permission": "update_cart"},
        {"role": "tester", "permission": "delete_cart"},
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
                    value["role"], value["permission"]
                )
            except EntityIntegrityError:
                pass
            except Exception as e:
                logger.error(f"Error seeding role: {e=}")

        logger.info("Seeding roles completed")
