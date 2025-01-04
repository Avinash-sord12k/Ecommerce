import httpx
from loguru import logger
from app.exceptions import EntityIntegrityError
from app.categories.repository import ProductCategoryRepository
from app.categories.models import CategoryCreateModel
from app.categories.schema import Category as ProductCategory


class Seeder(object):
    TABLE_NAME = ProductCategory.__tablename__
    API_URL = "https://dummyjson.com/products/categories"

    @staticmethod
    async def fetch_categories() -> list:
        """
        Fetch categories from the dummy API and filter the data.
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(Seeder.API_URL)
                response.raise_for_status()
                data = response.json()

                # Transform the response into a list of CategoryCreateModel instances
                categories = [
                    CategoryCreateModel(
                        name=category["name"],
                        slug=category["slug"],
                        description=f"Products in the {category['name']} category",
                        is_active=True,
                    )
                    for category in data
                ]
                logger.info("Fetched and transformed categories from the API")
                return categories
            except httpx.RequestError as e:
                logger.error(f"HTTP error while fetching categories: {str(e)}")
                raise
            except Exception as e:
                logger.error(
                    f"Error processing the fetched categories: {str(e)}"
                )
                raise

    @staticmethod
    async def run():
        """Run the category seeder"""
        repo = ProductCategoryRepository()
        try:
            # Fetch and filter category data
            categories = await Seeder.fetch_categories()
        except Exception as e:
            logger.error(f"Failed to fetch categories: {str(e)}")
            return

        for value in categories:
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
