from typing import List

from pydantic import BaseModel, ConfigDict, Field


class SubCategoryCreateSchema(BaseModel):
    name: str = Field(..., max_length=50, description="Name of the sub-category")
    category_id: int = Field(..., description="ID of the parent category")
    model_config = ConfigDict(from_attributes=True)


class SubCategoryResponseSchema(BaseModel):
    id: int = Field(..., description="ID of the sub-category")
    name: str = Field(..., max_length=50, description="Name of the sub-category")
    category_id: int = Field(..., description="ID of the parent category")
    model_config = ConfigDict(from_attributes=True)


class AllSubCategoriesResponseSchema(BaseModel):
    sub_categories: List[SubCategoryResponseSchema]
