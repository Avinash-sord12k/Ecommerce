from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_serializer
from typing_extensions import Annotated


class CreateProductRequestModel(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="The name of the product",
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Product description"
    )
    price: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)] = (
        Field(Decimal, description="Price of the product in INR")
    )
    slug: str = Field(
        str,
        min_length=3,
        max_length=60,
        description="Unique slug for the product",
    )
    tags: Optional[str] = Field(
        None, max_length=255, description="Comma-separated product tags"
    )
    discount: Annotated[
        Decimal, Field(ge=0, le=100, max_digits=4, decimal_places=2)
    ] = Field(0.0, description="Discount percentage")
    stock: Annotated[int, Field(ge=0)] = Field(
        ..., description="Available stock quantity"
    )
    category_id: int = Field(..., description="ID of the category")
    sub_category_ids: Optional[list[int]] = Field(
        None, description="List of sub-category IDs"
    )
    is_active: bool = Field(
        True, description="Indicates if the product is active"
    )
    model_config = ConfigDict(from_attributes=True)


class ProductResponseModel(BaseModel):
    id: int = Field(..., description="The unique identifier of the product")
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="The name of the product",
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Product description"
    )
    price: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)] = (
        Field(..., description="Price of the product")
    )
    slug: str = Field(
        str,
        min_length=3,
        max_length=60,
        description="Unique slug for the product",
    )
    tags: Optional[str] = Field(
        None, max_length=255, description="Comma-separated product tags"
    )
    discount: Annotated[
        Decimal, Field(ge=0, le=100, max_digits=4, decimal_places=2)
    ] = Field(0.0, description="Discount percentage")
    stock: Annotated[int, Field(ge=0)] = Field(
        ..., description="Available stock quantity"
    )
    category_id: int = Field(..., description="ID of the category")
    sub_category_ids: Optional[list[int]] = Field(
        None, description="List of sub-category IDs"
    )
    is_active: bool = Field(
        True, description="Indicates if the product is active"
    )
    model_config = ConfigDict(from_attributes=True)

    @field_serializer("price")
    def price_serializer(self, value: Decimal) -> str:
        return str(value)

    @field_serializer("discount")
    def discount_serializer(self, value: Decimal) -> str:
        return str(value)


class UpdateProductRequestModel(BaseModel):
    name: Optional[str] = Field(
        str,
        min_length=3,
        max_length=100,
        description="The name of the product",
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Product description"
    )
    price: Optional[
        Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]
    ] = Field(Decimal, description="Price of the product")
    slug: Optional[str] = Field(
        str,
        min_length=3,
        max_length=60,
        description="Unique slug for the product",
    )
    tags: Optional[str] = Field(
        str, max_length=255, description="Comma-separated product tags"
    )
    discount: Optional[
        Annotated[Decimal, Field(ge=0, le=100, max_digits=4, decimal_places=2)]
    ] = Field(0.0, description="Discount percentage")
    stock: Optional[Annotated[int, Field(ge=0)]] = Field(
        int, description="Available stock quantity"
    )
    category_id: Optional[int] = Field(None, description="ID of the category")
    sub_category_ids: Optional[list[int]] = Field(
        None, description="List of sub-category IDs"
    )
    is_active: Optional[bool] = Field(
        None, description="Indicates if the product is active"
    )
    model_config = ConfigDict(from_attributes=True)

    @field_serializer("price")
    def price_serializer(self, value: Decimal) -> str:
        return str(value)

    @field_serializer("discount")
    def discount_serializer(self, value: Decimal) -> str:
        return str(value)
