from loguru import logger

from app.exceptions import EntityIntegrityError
from app.categories.repository import ProductCategoryRepository
from app.categories.models import CategoryCreateModel
from app.categories.schema import Category as ProductCategory


class Seeder(object):
    TABLE_NAME = ProductCategory.__tablename__
    VALUES = [
        CategoryCreateModel(
            name="Electronics",
            description="Electronic devices and gadgets",
            slug="electronics",
            is_active=True,
        ),
        CategoryCreateModel(
            name="Clothing",
            description="Fashion and apparel items",
            slug="clothing",
            is_active=True,
        ),
        CategoryCreateModel(
            name="Books",
            description="Books, ebooks and publications",
            slug="books",
            is_active=True,
        ),
        CategoryCreateModel(
            name="Home & Garden",
            description="Home decor, furniture and garden supplies",
            slug="home-garden",
            is_active=True,
        ),
        CategoryCreateModel(
            name="Sports & Outdoors",
            description="Sporting goods and outdoor equipment",
            slug="sports-outdoors",
            is_active=True,
        ),
        CategoryCreateModel(
            name="Beauty & Health",
            description="Beauty products and health supplies",
            slug="beauty-health",
            is_active=True,
        ),
        CategoryCreateModel(
            name="Toys & Games",
            description="Toys, games and entertainment items",
            slug="toys-games",
            is_active=True,
        ),
    ]

    @staticmethod
    async def run():
        """Run the category seeder"""
        repo = ProductCategoryRepository()
        for value in Seeder.VALUES:
            try:
                await repo.create(value)
                logger.info(f"Created category: {value.name}")
            except EntityIntegrityError as e:
                logger.warning(
                    f"Category already exists: {value.name} - {str(e)}"
                )
            except Exception as e:
                logger.error(f"Error seeding category {value.name}: {str(e)}")

        logger.info("Category seeding completed")
