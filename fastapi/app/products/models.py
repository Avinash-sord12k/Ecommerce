from decimal import Decimal
from typing import Annotated, Literal, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_serializer,
)


class BaseProductModel(BaseModel):
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
    ] = Field(Decimal("0.0"), description="Discount percentage")
    tax: Annotated[
        Decimal, Field(ge=0, le=100, max_digits=4, decimal_places=2)
    ] = Field(Decimal("0.0"), description="Tax percentage")
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

    @field_serializer("price", "discount", "tax")
    def decimal_serializer(self, value: Decimal) -> str:
        return str(value)


class CreateProductRequestModel(BaseProductModel):
    model_config: ConfigDict = ConfigDict(from_attributes=True)


class ProductResponseModel(BaseProductModel):
    id: int = Field(..., description="The unique identifier of the product")
    model_config: ConfigDict = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def computed_price(self) -> Decimal:
        return self.price * (1 - self.discount / 100)


class UpdateProductRequestModel(BaseProductModel):
    model_config: ConfigDict = ConfigDict(from_attributes=True)


class ProductQueryParams(BaseModel):
    """Model for product query parameters"""

    # Basic fields
    id: Optional[int] = None
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    slug: Optional[str] = Field(None, min_length=3, max_length=60)

    # Price related
    min_price: Optional[Decimal] = Field(None, gt=0)
    max_price: Optional[Decimal] = Field(None, gt=0)
    min_discount: Optional[Decimal] = Field(None, ge=0, le=100)
    max_discount: Optional[Decimal] = Field(None, ge=0, le=100)
    min_tax: Optional[Decimal] = Field(None, ge=0, le=100)
    max_tax: Optional[Decimal] = Field(None, ge=0, le=100)

    # Stock related
    min_stock: Optional[int] = Field(None, ge=0)
    max_stock: Optional[int] = Field(None, ge=0)

    # Category related
    category_id: Optional[int] = None
    sub_category_id: Optional[int] = None

    # Other filters
    tags: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None

    # Sorting
    sort_by: Optional[
        Literal[
            "id",
            "name",
            "slug",
            "price",
            "discount",
            "tax",
            "stock",
            "created_at",
        ]
    ] = None
    sort_order: Optional[Literal["asc", "desc"]] = "asc"

    model_config: ConfigDict = ConfigDict(from_attributes=True)

    def to_filter_dict(self) -> dict:
        """Convert the model to a dictionary of non-None values"""
        return {k: v for k, v in self.model_dump().items() if v is not None}
