from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class CreateProductRequestSchema(BaseModel):
    name: str = Field(..., max_length=100, description="The name of the product")
    description: Optional[str] = Field(None, max_length=500, description="Product description")
    price: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)] = Field(
        ..., description="Price of the product in INR"
    )
    slug: str = Field(..., max_length=60, description="Unique slug for the product")
    tags: Optional[str] = Field(None, max_length=255, description="Comma-separated product tags")
    discount: Annotated[Decimal, Field(ge=0, le=100, max_digits=4, decimal_places=2)] = Field(
        0.0, description="Discount percentage"
    )
    stock: Annotated[int, Field(ge=0)] = Field(..., description="Available stock quantity")
    category_id: int = Field(..., description="ID of the category")
    sub_category_id: Optional[int] = Field(None, description="ID of the sub-category")
    is_active: bool = Field(True, description="Indicates if the product is active")
    model_config = ConfigDict(from_attributes=True)


class ProductResponseSchema(BaseModel):
    id: int = Field(..., description="The unique identifier of the product")
    name: str = Field(..., max_length=100, description="The name of the product")
    description: Optional[str] = Field(None, max_length=500, description="Product description")
    price: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)] = Field(
        ..., description="Price of the product"
    )
    slug: str = Field(..., max_length=60, description="Unique slug for the product")
    tags: Optional[str] = Field(None, max_length=255, description="Comma-separated product tags")
    discount: Annotated[Decimal, Field(ge=0, le=100, max_digits=4, decimal_places=2)] = Field(
        0.0, description="Discount percentage"
    )
    stock: Annotated[int, Field(ge=0)] = Field(..., description="Available stock quantity")
    category_id: int = Field(..., description="ID of the category")
    sub_category_id: Optional[int] = Field(None, description="ID of the sub-category")
    is_active: bool = Field(True, description="Indicates if the product is active")
    model_config = ConfigDict(from_attributes=True)


class UpdateProductRequestSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=100, description="The name of the product")
    description: Optional[str] = Field(None, max_length=500, description="Product description")
    price: Optional[Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]] = Field(
        None, description="Price of the product"
    )
    slug: Optional[str] = Field(None, max_length=60, description="Unique slug for the product")
    tags: Optional[str] = Field(None, max_length=255, description="Comma-separated product tags")
    discount: Optional[Annotated[Decimal, Field(ge=0, le=100, max_digits=4, decimal_places=2)]] = Field(
        None, description="Discount percentage"
    )
    stock: Optional[Annotated[int, Field(ge=0)]] = Field(None, description="Available stock quantity")
    category_id: Optional[int] = Field(None, description="ID of the category")
    sub_category_id: Optional[int] = Field(None, description="ID of the sub-category")
    is_active: Optional[bool] = Field(None, description="Indicates if the product is active")
    model_config = ConfigDict(from_attributes=True)
