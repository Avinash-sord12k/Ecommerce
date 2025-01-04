import httpx
from decimal import Decimal
from loguru import logger
from app.exceptions import EntityIntegrityError
from app.products.repository import ProductRepository
from app.products.models import CreateProductRequestModel
from app.products.schema import Product
from app.categories.repository import (
    ProductCategoryRepository as CategoryRepository,
)  # Assuming you have a CategoryRepository


class Seeder(object):
    TABLE_NAME = Product.__tablename__

    # Fetch product data from the API
    @staticmethod
    async def fetch_api_data():
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://dummyjson.com/products")
                logger.info(f"API response status code: {response.json()}")
                response.raise_for_status()  # Will raise an error for bad status codes
                return response.json()["products"]
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e}")
        except Exception as e:
            logger.error(f"An error occurred while fetching data: {e}")
        return []

    # Convert API data to CreateProductRequestModel
    @staticmethod
    def map_product_data(
        api_product: dict, category_id: int
    ) -> CreateProductRequestModel:
        # Map fields from the API response to the CreateProductRequestModel
        logger.info(f"Mapping product: {api_product.get('thumbnail', '')}")
        logger.info(f"Mapping product: {api_product.get('images', [])}")
        return CreateProductRequestModel(
            name=api_product["title"],
            price=Decimal(str(api_product["price"])),
            discount=Decimal(str(api_product["discountPercentage"])),
            tax=Decimal(
                "5.0"
            ),  # Default tax value, you can adjust as necessary
            slug=api_product["sku"],  # Assuming SKU as a slug
            description=api_product["description"],
            category_id=category_id,  # Use the category_id fetched from the DB
            stock=api_product["stock"],
            sub_category_ids=[],  # You can add logic to map sub-categories
            tags=",".join(
                api_product["tags"]
            ),  # Convert tags to a comma-separated string
            is_active=True,
            thumbnail=api_product.get("thumbnail", ""),  # Thumbnail URL
            images=api_product.get("images", []),  # Images list
        )

    # Fetch category ID by category name
    @staticmethod
    async def get_category_id_by_name(category_name: str) -> int:
        category_repo = CategoryRepository()
        category = await category_repo.get_by_name(
            category_name
        )  # Assuming you have this method in CategoryRepository
        if category:
            return category.get("id")
        return None

    @staticmethod
    async def run(user_id: int = 1):
        repo = ProductRepository()
        products = await Seeder.fetch_api_data()

        for api_product in products:
            # Fetch the category ID based on the category name from the API product
            category_id = await Seeder.get_category_id_by_name(
                api_product["category"]
            )

            if not category_id:
                logger.warning(
                    f"Category '{api_product['category']}' not found. Skipping product '{api_product['title']}'"
                )
                continue  # Skip the product if category is not found

            try:
                # Map the API product data to our model, using the correct category ID
                product_data = Seeder.map_product_data(
                    api_product, category_id
                )

                # Create the product in the database
                await repo.create(user_id=user_id, product=product_data)
                logger.info(f"Created product: {product_data.name}")
            except EntityIntegrityError as e:
                logger.warning(
                    f"Product already exists: {product_data.name} - {str(e)}"
                )
            except Exception as e:
                logger.error(
                    f"Error seeding product {product_data.name}: {str(e)}"
                )

        logger.info("Product seeding completed")
