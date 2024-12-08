from typing import List

from pydantic import BaseModel, ConfigDict, Field


class CategoryCreateModel(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Name of the category")
    model_config = ConfigDict(from_attributes=True)


class CategoryResponseModel(BaseModel):
    id: int = Field(..., description="ID of the category")
    name: str = Field(..., min_length=3, max_length=50, description="Name of the category")
    model_config = ConfigDict(from_attributes=True)


class AllCategoriesResponseModel(BaseModel):
    categories: List[CategoryResponseModel]
