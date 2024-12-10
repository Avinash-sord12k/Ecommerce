from sqlalchemy import delete, insert, select
from sqlalchemy.exc import IntegrityError

from app.categories.models import (
    AllCategoriesResponseModel,
    CategoryCreateModel,
)
from app.categories.schema import Category
from app.database import DatabaseManager
from app.exceptions import EntityIntegrityError, EntityNotFoundError


class ProductCategoryRepository:
    def __init__(self) -> None:
        self.db = DatabaseManager._instance

    async def create(self, category: CategoryCreateModel):
        async with self.db.engine.begin() as connection:
            try:
                result = await connection.execute(
                    insert(Category).values(name=category.name)
                )
                await connection.commit()
                return {
                    "id": result.inserted_primary_key[0],
                    "name": category.name,
                }
            except IntegrityError:
                raise EntityIntegrityError(entity="Category")

    async def get_by_id(self, id: int) -> Category:
        async with self.db.engine.begin() as connection:
            result = await connection.execute(
                select(Category).where(Category.id == id)
            )
            category = result.fetchone()
            if category is None:
                raise EntityNotFoundError(entity="Category")

            return category._asdict()

    async def get_all(self) -> AllCategoriesResponseModel:
        async with self.db.engine.begin() as connection:
            result = await connection.execute(select(Category))
            categories = result.fetchall()
            return AllCategoriesResponseModel(
                categories=[
                    {"id": category.id, "name": category.name}
                    for category in categories
                ]
            )

    async def delete(self, id: int):
        async with self.db.engine.begin() as connection:
            result = await connection.execute(
                select(Category).where(Category.id == id)
            )
            if not (category := result.fetchone()):
                raise EntityNotFoundError(entity="Category")

            await connection.execute(
                delete(Category).where(Category.id == category.id)
            )
            await connection.commit()
            return category._asdict()
