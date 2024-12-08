from sqlalchemy import insert, select, update, delete

from app.database import DatabaseManager
from app.exceptions import EntityNotFoundError
from app.category.repository import ProductCategoryRepository
from app.subcategory.repository import ProductSubCategoryRepository
from app.subcategory.schema import product_subcategory_association
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
            # Check if the category exist
            category_repo = ProductCategoryRepository()
            await category_repo.get_by_id(product.category_id)

            # Check if the subcategory exist
            sub_category_repo = ProductSubCategoryRepository()
            for sub_category_id in product.sub_category_ids:
                await sub_category_repo.get_by_id(sub_category_id)

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
                is_active=product.is_active,
            )
            result = await connection.execute(q)
            created_product_id = result.inserted_primary_key[0]

            for sub_category_id in product.sub_category_ids:
                q = insert(product_subcategory_association).values(
                    product_id=created_product_id,
                    sub_category_id=sub_category_id,
                )
                result = await connection.execute(q)

            await connection.commit()
            return created_product_id

    async def update(
        self, product_id: int, product_update: UpdateProductRequestSchema
    ) -> ProductResponseSchema:
        async with self.db.engine.begin() as connection:
            # Delete all the existing sub-category associations
            q = delete(product_subcategory_association).where(
                product_subcategory_association.c.product_id == product_id
            )
            await connection.execute(q)

            # bulk create the new sub-category associations
            values = [
                {"product_id": product_id, "sub_category_id": sub_category_id}
                for sub_category_id in product_update.sub_category_ids
            ]
            q = insert(product_subcategory_association).values(values)
            await connection.execute(q)

            # Update the product
            q = (
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
                    is_active=product_update.is_active,
                )
            )
            await connection.execute(q)
            await connection.commit()
            return product_update.model_dump()

    async def get_by_id(self, product_id: int) -> ProductResponseSchema:
        async with self.db.engine.begin() as connection:
            q = select(Product).where(Product.id == product_id)
            result = await connection.execute(q)
            product = result.fetchone()
            if not product:
                raise EntityNotFoundError(entity="Product")

            return product._asdict()

    async def get_by_category_id(
        self, category_id: int, max_objects: int = 10
    ) -> list[ProductResponseSchema]:
        async with self.db.engine.begin() as connection:
            q = (
                select(Product)
                .where(Product.category_id == category_id)
                .limit(max_objects)
            )
            result = await connection.execute(q)
            products = result.fetchall()
            if not products:
                raise EntityNotFoundError(entity="Product")

            return [product._asdict() for product in products]

    async def get_by_category_name(
        self, category_name: str, max_objects: int = 10
    ) -> list[ProductResponseSchema]:
        async with self.db.engine.begin() as connection:
            q = (
                select(Product)
                .where(Product.category.has(name=category_name))
                .limit(max_objects)
            )
            result = await connection.execute(q)
            products = result.fetchall()
            if not products:
                raise EntityNotFoundError(entity="Product")

            return [product._asdict() for product in products]

    async def get_by_sub_category_id(
        self, sub_category_id: int, max_objects: int = 10
    ) -> list[ProductResponseSchema]:
        async with self.db.engine.begin() as connection:
            q = (
                select(Product)
                .where(Product.sub_category_id == sub_category_id)
                .limit(max_objects)
            )
            result = await connection.execute(q)
            products = result.fetchall()
            if not products:
                raise EntityNotFoundError(entity="Product")

            return [product._asdict() for product in products]

    async def get_by_sub_category_name(
        self, sub_category_name: str, max_objects: int = 10
    ) -> list[ProductResponseSchema]:
        async with self.db.engine.begin() as connection:
            q = (
                select(Product)
                .where(Product.sub_category.has(name=sub_category_name))
                .limit(max_objects)
            )
            result = await connection.execute(q)
            products = result.fetchall()
            if not products:
                raise EntityNotFoundError(entity="Product")

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
