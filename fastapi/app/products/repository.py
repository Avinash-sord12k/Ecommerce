from sqlalchemy import insert, select, update

from app.database import DatabaseManager
from app.products.models import Product
from app.products.schema import (
    CreateProductRequestSchema,
    UpdateProductRequestSchema,
)


class ProductRepository:
    def __init__(self):
        self.db = DatabaseManager._instance

    async def create(self, product: CreateProductRequestSchema):
        async with self.db.engine.begin() as connection:
            # Create a new product in the database
            result = await connection.execute(
                insert(Product).values(
                    name=product.name,
                    description=product.description,
                    price=product.price,
                    slug=product.slug,
                    tags=product.tags,
                    discount=product.discount,
                    stock=product.stock,
                    category_id=product.category_id,
                    sub_category_id=product.sub_category_id,
                    is_active=product.is_active,
                )
            )
            created_product_id = result.inserted_primary_key[0]
            return created_product_id

    async def update(self, product_id: int, product_update: UpdateProductRequestSchema):
        async with self.db.engine.begin() as connection:
            stmt = (
                update(Product)
                .where(Product.id == product_id)
                .values(
                    name=product_update.name,
                    description=product_update.description,
                    price=product_update.price,
                    slug=product_update.slug,
                    tags=product_update.tags,
                    discount=product_update.discount,
                    stock=product_update.stock,
                    category_id=product_update.category_id,
                    sub_category_id=product_update.sub_category_id,
                    is_active=product_update.is_active,
                )
            )

            result = await connection.execute(stmt)
            if result.rowcount == 0:
                return None

            updated_product = await connection.execute(select(Product).where(Product.id == product_id))
            return updated_product.scalars().first()
