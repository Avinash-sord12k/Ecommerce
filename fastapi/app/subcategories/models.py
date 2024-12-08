from typing import List

from pydantic import BaseModel, ConfigDict, Field


class SubCategoryCreateModel(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Name of the sub-category")
    category_id: int = Field(..., description="ID of the parent category")
    model_config = ConfigDict(from_attributes=True)


class SubCategoryResponseModel(BaseModel):
    id: int = Field(..., description="ID of the sub-category")
    name: str = Field(..., min_length=3, max_length=50, description="Name of the sub-category")
    category_id: int = Field(..., description="ID of the parent category")
    model_config = ConfigDict(from_attributes=True)


class AllSubCategoriesResponseModel(BaseModel):
    sub_categories: List[SubCategoryResponseModel]
