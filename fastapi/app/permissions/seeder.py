from loguru import logger

from app.address.permissions import PERMISSIONS as ADDRESS_PERMISSIONS
from app.cart.permissions import PERMISSIONS as CART_PERMISSIONS
from app.categories.permissions import PERMISSIONS as CATEGORY_PERMISSIONS
from app.exceptions import EntityIntegrityError
from app.permissions.permissions import PERMISSIONS as PERMISSION_PERMISSIONS
from app.permissions.repository import PermissionRepository
from app.permissions.schema import Permission
from app.products.permissions import PERMISSIONS as PRODUCT_PERMISSIONS
from app.roles.permissions import PERMISSIONS as ROLE_PERMISSIONS
from app.subcategories.permissions import (
    PERMISSIONS as SUBCATEGORY_PERMISSIONS,
)


class Seeder:
    TABLE_NAME = Permission.__tablename__
    VALUES = [
        *ROLE_PERMISSIONS,
        *PERMISSION_PERMISSIONS,
        *CATEGORY_PERMISSIONS,
        *SUBCATEGORY_PERMISSIONS,
        *PRODUCT_PERMISSIONS,
        *CART_PERMISSIONS,
        *ADDRESS_PERMISSIONS,
    ]

    async def run(self):
        # delete all permission from existing table
        repo = PermissionRepository()
        for value in self.VALUES:
            try:
                await repo.create(value)
            except EntityIntegrityError:
                pass
            except Exception as e:
                logger.error(f"Error seeding permission: {e=}")

        logger.info("Seeding permissions completed")
