from typing import Optional

from pydantic import BaseModel, Field, condecimal, conint


class CreateProductRequestSchema(BaseModel):
    name: str = Field(
        ..., max_length=100, description="The name of the product"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Product description"
    )
    price: condecimal(gt=0, max_digits=10, decimal_places=2) = Field(
        ..., description="Price of the product in INR"
    )
    slug: str = Field(
        ..., max_length=60, description="Unique slug for the product"
    )
    tags: Optional[str] = Field(
        None, max_length=255, description="Comma-separated product tags"
    )
    discount: condecimal(ge=0, le=100, max_digits=4, decimal_places=2) = Field(
        0.0, description="Discount percentage"
    )
    stock: conint(ge=0) = Field(..., description="Available stock quantity")
    category_id: int = Field(..., description="ID of the category")
    sub_category_id: Optional[int] = Field(
        None, description="ID of the sub-category"
    )
    is_active: bool = Field(
        True, description="Indicates if the product is active"
    )

    class Config:
        from_attributes = True


class ProductResponseSchema(BaseModel):
    id: int = Field(..., description="The unique identifier of the product")
    name: str = Field(
        ..., max_length=100, description="The name of the product"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Product description"
    )
    price: condecimal(gt=0, max_digits=10, decimal_places=2) = Field(
        ..., description="Price of the product"
    )
    slug: str = Field(
        ..., max_length=60, description="Unique slug for the product"
    )
    tags: Optional[str] = Field(
        None, max_length=255, description="Comma-separated product tags"
    )
    discount: condecimal(ge=0, le=100, max_digits=4, decimal_places=2) = Field(
        0.0, description="Discount percentage"
    )
    stock: conint(ge=0) = Field(..., description="Available stock quantity")
    category_id: int = Field(..., description="ID of the category")
    sub_category_id: Optional[int] = Field(
        None, description="ID of the sub-category"
    )
    is_active: bool = Field(
        True, description="Indicates if the product is active"
    )

    class Config:
        from_attributes = True


class UpdateProductRequestSchema(BaseModel):
    name: Optional[str] = Field(
        None, max_length=100, description="The name of the product"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Product description"
    )
    price: Optional[condecimal(gt=0, max_digits=10, decimal_places=2)] = Field(
        None, description="Price of the product"
    )
    slug: Optional[str] = Field(
        None, max_length=60, description="Unique slug for the product"
    )
    tags: Optional[str] = Field(
        None, max_length=255, description="Comma-separated product tags"
    )
    discount: Optional[
        condecimal(ge=0, le=100, max_digits=4, decimal_places=2)
    ] = Field(None, description="Discount percentage")
    stock: Optional[conint(ge=0)] = Field(
        None, description="Available stock quantity"
    )
    category_id: Optional[int] = Field(None, description="ID of the category")
    sub_category_id: Optional[int] = Field(
        None, description="ID of the sub-category"
    )
    is_active: Optional[bool] = Field(
        None, description="Indicates if the product is active"
    )

    class Config:
        from_attributes = True


class CategoryCreateSchema(BaseModel):
    name: str = Field(..., max_length=50, description="Name of the category")

    class Config:
        from_attributes = True


class CategoryResponseSchema(BaseModel):
    id: int = Field(..., description="ID of the category")
    name: str = Field(..., max_length=50, description="Name of the category")

    class Config:
        from_attributes = True


class SubCategoryCreateSchema(BaseModel):
    name: str = Field(
        ..., max_length=50, description="Name of the sub-category"
    )
    category_id: int = Field(..., description="ID of the parent category")

    class Config:
        from_attributes = True


class SubCategoryResponseSchema(BaseModel):
    id: int = Field(..., description="ID of the sub-category")
    name: str = Field(
        ..., max_length=50, description="Name of the sub-category"
    )
    category_id: int = Field(..., description="ID of the parent category")

    class Config:
        from_attributes = True
