from loguru import logger
from sqlalchemy import delete, insert, select, update

from app.categories.repository import ProductCategoryRepository
from app.database import DatabaseManager
from app.exceptions import EntityNotFoundError
from app.products.models import (
    CreateProductRequestModel,
    UpdateProductRequestModel,
)
from app.products.schema import Product
from app.repository import BaseRepository
from app.subcategories.repository import ProductSubCategoryRepository
from app.subcategories.schema import (
    SubCategory,
    product_subcategory_association,
)


class ProductRepository(BaseRepository):
    def __init__(self):
        super().__init__(DatabaseManager._instance)

    async def create(
        self, user_id: int, product: CreateProductRequestModel
    ) -> int:
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
                user_id=user_id,
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
        self, product_id: int, product_update: UpdateProductRequestModel
    ) -> dict:
        async with self.db.engine.begin() as connection:
            # Check if the product exist
            q = select(Product).where(Product.id == product_id)
            result = await connection.execute(q)
            if not (_ := result.fetchone()):
                raise EntityNotFoundError(entity="Product")

            # Delete all the existing sub-category associations
            q = delete(product_subcategory_association).where(
                product_subcategory_association.c.product_id == product_id
            )
            logger.debug(f"Delete existing associations: {q}")
            await connection.execute(q)

            # bulk create the new sub-category associations
            values = [
                {"product_id": product_id, "sub_category_id": sub_category_id}
                for sub_category_id in product_update.sub_category_ids
            ]
            logger.debug(f"Insert new associations: {values}")
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
            logger.debug(f"Update product: {q}")
            await connection.commit()
            return product_update.model_dump()

    async def get_by_id(self, product_id: int) -> dict:
        async with self.db.engine.begin() as connection:
            q = select(Product).where(Product.id == product_id)
            result = await connection.execute(q)
            product = result.fetchone()
            if not product:
                raise EntityNotFoundError(entity="Product")

            return product._asdict()

    async def get_by_category_id(
        self, category_id: int, page: int = 1, page_size: int = 10
    ) -> tuple[list[dict], int]:
        query = select(Product).where(Product.category_id == category_id)
        items, total = await self.get_paginated(query, page, page_size)

        if not items:
            raise EntityNotFoundError(entity="Product")
        return items, total

    async def get_by_category_name(
        self, category_name: str, page: int = 1, page_size: int = 10
    ) -> tuple[list[dict], int]:
        query = select(Product).where(Product.category.has(name=category_name))
        items, total = await self.get_paginated(query, page, page_size)

        if not items:
            raise EntityNotFoundError(entity="Product")
        return items, total

    async def get_by_subcategory_id(
        self, sub_category_id: int, page: int = 1, page_size: int = 10
    ) -> tuple[list[dict], int]:
        association_query = select(
            product_subcategory_association.c.product_id
        ).where(
            product_subcategory_association.c.sub_category_id
            == sub_category_id
        )

        query = select(Product).where(
            Product.id.in_(association_query.scalar_subquery())
        )

        items, total = await self.get_paginated(query, page, page_size)

        if not items:
            logger.debug("No associations found")
            raise EntityNotFoundError(entity="Product")

        return items, total

    async def get_by_sub_category_name(
        self, sub_category_name: str, page: int = 1, page_size: int = 10
    ) -> tuple[list[dict], int]:
        association_query = (
            select(product_subcategory_association.c.product_id)
            .join(
                SubCategory,
                product_subcategory_association.c.sub_category_id
                == SubCategory.id,
            )
            .where(SubCategory.name == sub_category_name)
        )

        query = select(Product).where(
            Product.id.in_(association_query.scalar_subquery())
        )

        items, total = await self.get_paginated(query, page, page_size)

        if not items:
            raise EntityNotFoundError(entity="Product")
        return items, total

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
