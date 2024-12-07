from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.database import DatabaseManager
from app.exceptions import EntityIntegrityError, EntityNotFoundError
from app.subcategory.models import SubCategory
from app.subcategory.schema import (
    AllSubCategoriesResponseSchema,
    SubCategoryCreateSchema,
)


class ProductSubCategoryRepository:
    def __init__(self) -> None:
        self.db = DatabaseManager._instance

    async def create(self, sub_category: SubCategoryCreateSchema):
        async with self.db.engine.begin() as connection:
            try:
                result = (
                    await connection.execute(select(Category).where(Category.id == sub_category.category_id))
                ).one()
            except NoResultFound:
                raise EntityNotFoundError(entity="Category")

            try:
                result = await connection.execute(
                    insert(SubCategory).values(
                        name=sub_category.name,
                        category_id=sub_category.category_id,
                    )
                )
                await connection.commit()
                return {
                    "id": result.inserted_primary_key[0],
                    "name": sub_category.name,
                    "category_id": sub_category.category_id,
                }
            except IntegrityError:
                raise EntityIntegrityError(entity="Sub-Category")

    async def get_all(self) -> AllSubCategoriesResponseSchema:
        async with self.db.engine.begin() as connection:
            result = await connection.execute(select(SubCategory))
            sub_categories = result.fetchall()
            return AllSubCategoriesResponseSchema(
                sub_categories=[
                    {
                        "id": sub_category.id,
                        "name": sub_category.name,
                        "category_id": sub_category.category_id,
                    }
                    for sub_category in sub_categories
                ]
            )
