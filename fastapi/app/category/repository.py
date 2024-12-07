from sqlalchemy import delete, insert, select
from sqlalchemy.exc import IntegrityError

from app.category.models import Category
from app.category.schema import (
    AllCategoriesResponseSchema,
    CategoryCreateSchema,
)
from app.database import DatabaseManager
from app.exceptions import EntityIntegrityError, EntityNotFoundError


class ProductCategoryRepository:
    def __init__(self) -> None:
        self.db = DatabaseManager._instance

    async def create(self, category: CategoryCreateSchema):
        async with self.db.engine.begin() as connection:
            try:
                result = await connection.execute(insert(Category).values(name=category.name))
                await connection.commit()
                return {
                    "id": result.inserted_primary_key[0],
                    "name": category.name,
                }
            except IntegrityError:
                raise EntityIntegrityError(entity="Category")

    async def get_by_id(self, id: int) -> Category:
        async with self.db.engine.begin() as connection:
            result = await connection.execute(select(Category).where(Category.id == id))
            category = result.fetchone()
            if category is None:
                raise EntityNotFoundError(entity="Category")

            return category._asdict()

    async def get_all(self) -> AllCategoriesResponseSchema:
        async with self.db.engine.begin() as connection:
            result = await connection.execute(select(Category))
            categories = result.fetchall()
            return AllCategoriesResponseSchema(
                categories=[{"id": category.id, "name": category.name} for category in categories]
            )

    async def delete(self, id: int):
        async with self.db.engine.begin() as connection:
            result = await connection.execute(select(Category).where(Category.id == id))
            if not (category := result.fetchone()):
                raise EntityNotFoundError(entity="Category")

            await connection.execute(delete(Category).where(Category.id == category.id))
            await connection.commit()
            return category._asdict()
