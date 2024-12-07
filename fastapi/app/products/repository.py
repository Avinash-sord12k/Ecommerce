from sqlalchemy import insert, select, update, delete

from app.database import DatabaseManager
from app.exceptions import EntityNotFoundError
from app.products.schema import Product
from app.products.models import (
    CreateProductRequestSchema,
    UpdateProductRequestSchema,
    ProductResponseSchema,
)


class ProductRepository:
    def __init__(self):
        self.db = DatabaseManager._instance

    async def create(self, product: CreateProductRequestSchema) -> int:
        async with self.db.engine.begin() as connection:
            # Create a new product in the database
            q = insert(Product).values(
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
            result = await connection.execute(q)
            await connection.commit()

            created_product_id = result.inserted_primary_key[0]
            return created_product_id

    async def update(self, product_id: int, product_update: UpdateProductRequestSchema) -> ProductResponseSchema:
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

            await connection.execute(stmt)
            await connection.commit()
            return product_update.model_dump()

    async def get_by_id(self, product_id: int) -> ProductResponseSchema:
        async with self.db.engine.begin() as connection:
            q = select(Product).where(Product.id == product_id)
            result = await connection.execute(q)
            product = result.fetchone()
            if product is None:
                raise EntityNotFoundError(entity="Product")

            return product._asdict()

    async def get_by_category_id(self, category_id: int, max_objects: int = 10) -> list[ProductResponseSchema]:
        async with self.db.engine.begin() as connection:
            q = select(Product).where(Product.category_id == category_id).limit(max_objects)
            result = await connection.execute(q)
            products = result.fetchall()
            return [product._asdict() for product in products]

    async def get_by_category_name(self, category_name: str, max_objects: int = 10) -> list[ProductResponseSchema]:
        async with self.db.engine.begin() as connection:
            q = select(Product).where(Product.category.has(name=category_name)).limit(max_objects)
            result = await connection.execute(q)
            products = result.fetchall()
            return [product._asdict() for product in products]

    async def get_by_sub_category_id(self, sub_category_id: int, max_objects: int = 10) -> list[ProductResponseSchema]:
        async with self.db.engine.begin() as connection:
            q = select(Product).where(Product.sub_category_id == sub_category_id).limit(max_objects)
            result = await connection.execute(q)
            products = result.fetchall()
            return [product._asdict() for product in products]

    async def get_by_sub_category_name(
        self, sub_category_name: str, max_objects: int = 10
    ) -> list[ProductResponseSchema]:
        async with self.db.engine.begin() as connection:
            q = select(Product).where(Product.sub_category.has(name=sub_category_name)).limit(max_objects)
            result = await connection.execute(q)
            products = result.fetchall()
            return [product._asdict() for product in products]

    async def delete(self, id: int):
        async with self.db.engine.begin() as connection:
            q = select(Product).where(Product.id == id)
            result = await connection.execute(q)
            if not (product := result.fetchone()):
                raise EntityNotFoundError(entity="Product")

            q = delete(Product).where(Product.id == product.id)
            await connection.execute(q)
            await connection.commit()
            return product._asdict()
