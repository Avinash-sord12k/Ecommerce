from typing import List

from pydantic import BaseModel, ConfigDict, Field


class CategoryCreateSchema(BaseModel):
    name: str = Field(..., max_length=50, description="Name of the category")
    model_config = ConfigDict(from_attributes=True)


class CategoryResponseSchema(BaseModel):
    id: int = Field(..., description="ID of the category")
    name: str = Field(..., max_length=50, description="Name of the category")
    model_config = ConfigDict(from_attributes=True)


class AllCategoriesResponseSchema(BaseModel):
    categories: List[CategoryResponseSchema]
