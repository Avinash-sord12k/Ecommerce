from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
)

from app.cart.schema import CartStatus


class CreateCartRequestModel(BaseModel):
    name: str = Field(
        ..., min_length=3, max_length=50, description="Name of the cart"
    )
    reminder_date: Optional[datetime] = Field(
        None, description="Reminder date of the cart"
    )

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("reminder_date")
    def serialize_reminder_date(self, value: datetime):
        return str(value)

    @field_validator("reminder_date")
    @classmethod
    def validate_reminder_date(cls, value: datetime):
        v_timezone = value.tzinfo
        current_relative_time = datetime.now(tz=v_timezone)
        if value < current_relative_time:
            raise ValueError("Reminder date cannot be in the past")
        return value


class CartResponseModel(BaseModel):
    id: int = Field(..., description="ID of the cart")


class AddToCartRequestModel(BaseModel):
    cart_id: int = Field(..., description="ID of the cart")
    product_id: int = Field(..., description="ID of the product")
    quantity: int = Field(..., le=10, description="Quantity of the product")

    model_config = ConfigDict(from_attributes=True)


class CartsResponseModel(BaseModel):
    id: int = Field(..., description="ID of the cart")
    name: str = Field(..., description="Name of the cart")
    reminder_date: Optional[datetime] = Field(
        None, description="Reminder date of the cart"
    )
    status: CartStatus = Field(..., description="Status of the cart")

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("reminder_date")
    def serialize_reminder_date(self, value: datetime):
        return str(value)


class AllCartsResponseModel(BaseModel):
    carts: list[CartsResponseModel]

    model_config = ConfigDict(from_attributes=True)


class CartItemsResponseModel(BaseModel):
    id: int = Field(..., description="ID of the cart item")
    product_id: int = Field(..., description="ID of the product")
    quantity: int = Field(..., description="Quantity of the product")

    model_config = ConfigDict(from_attributes=True)


class SingleCartResponseModel(CartsResponseModel):
    items: list[CartItemsResponseModel]

    model_config = ConfigDict(from_attributes=True)
