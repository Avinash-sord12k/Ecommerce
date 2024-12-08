from sqlalchemy import insert, select, delete
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.database import DatabaseManager
from app.exceptions import EntityIntegrityError, EntityNotFoundError
from app.categories.schema import Category
from app.subcategories.schema import SubCategory
from app.subcategories.models import (
    AllSubCategoriesResponseModel,
    SubCategoryCreateModel,
)


class ProductSubCategoryRepository:
    def __init__(self) -> None:
        self.db = DatabaseManager._instance

    async def create(self, sub_category: SubCategoryCreateModel):
        async with self.db.engine.begin() as connection:
            try:
                # check if the category exists
                q = select(Category).where(
                    Category.id == sub_category.category_id
                )
                result = (await connection.execute(q)).one()
            except NoResultFound:
                raise EntityNotFoundError(entity="Category")

            try:
                # create the subcategory
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

    async def get_by_id(self, id: int) -> SubCategory:
        async with self.db.engine.begin() as connection:
            q = select(SubCategory).where(SubCategory.id == id)
            result = await connection.execute(q)
            sub_category = result.fetchone()
            if sub_category is None:
                raise EntityNotFoundError(entity="Sub-Category")

            return sub_category._asdict()

    async def get_all(self) -> AllSubCategoriesResponseModel:
        async with self.db.engine.begin() as connection:
            result = await connection.execute(select(SubCategory))
            sub_categories = result.fetchall()
            return AllSubCategoriesResponseModel(
                sub_categories=[
                    {
                        "id": sub_category.id,
                        "name": sub_category.name,
                        "category_id": sub_category.category_id,
                    }
                    for sub_category in sub_categories
                ]
            )

    async def delete(self, id: int):
        async with self.db.engine.begin() as connection:
            q = select(SubCategory).where(SubCategory.id == id)
            result = await connection.execute(q)
            if not (sub_category := result.fetchone()):
                raise EntityNotFoundError(entity="Sub-Category")

            q = delete(SubCategory).where(SubCategory.id == sub_category.id)
            await connection.execute(q)
            await connection.commit()
            return sub_category._asdict()
