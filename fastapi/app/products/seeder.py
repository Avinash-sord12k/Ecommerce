from decimal import Decimal
from loguru import logger

from app.exceptions import EntityIntegrityError
from app.products.repository import ProductRepository
from app.products.models import CreateProductRequestModel
from app.products.schema import Product


class Seeder(object):
    TABLE_NAME = Product.__tablename__
    VALUES = [
        CreateProductRequestModel(
            name="Gaming Laptop XPS-15",
            price=Decimal("1299.99"),
            discount=Decimal("10.0"),
            tax=Decimal("5.0"),
            slug="gaming-laptop-xps-15",
            description="High-performance gaming laptop with RTX 3080",
            category_id=11,
            stock=50,
            sub_category_ids=[],
            tags="laptop, gaming, electronics",
            is_active=True,
        ),
        CreateProductRequestModel(
            name="Smartphone Pro Max",
            price=Decimal("999.99"),
            discount=Decimal("5.0"),
            tax=Decimal("5.0"),
            slug="smartphone-pro-max",
            description="Latest flagship smartphone with 5G capability",
            category_id=11,
            stock=100,
            sub_category_ids=[],
            tags="smartphone, mobile, electronics",
            is_active=True,
        ),
        CreateProductRequestModel(
            name="Wireless Earbuds Pro",
            price=Decimal("199.99"),
            discount=Decimal("15.0"),
            tax=Decimal("5.0"),
            slug="wireless-earbuds-pro",
            description="Premium wireless earbuds with noise cancellation",
            category_id=11,
            stock=200,
            sub_category_ids=[],
            tags="earbuds, audio, electronics",
            is_active=True,
        ),
    ]

    @staticmethod
    async def run(user_id: int = 1):
        repo = ProductRepository()
        for value in Seeder.VALUES:
            try:
                await repo.create(user_id=user_id, product=value)
                logger.info(f"Created product: {value.name}")
            except EntityIntegrityError as e:
                logger.warning(
                    f"Product already exists: {value.name} - {str(e)}"
                )
            except Exception as e:
                logger.error(f"Error seeding product {value.name}: {str(e)}")

        logger.info("Product seeding completed")
