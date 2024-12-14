from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

from app.cart.schema import CartStatus


class CreateCartRequestModel(BaseModel):
    name: str = Field(..., description="Name of the cart")
    reminder_date: Optional[datetime] = Field(
        None, description="Reminder date of the cart"
    )

    model_config = ConfigDict(from_attributes=True)


class CartResponseModel(BaseModel):
    id: int = Field(..., description="ID of the cart")


class AddToCartRequestModel(BaseModel):
    product_id: int = Field(..., description="ID of the product")
    quantity: int = Field(..., description="Quantity of the product")

    model_config = ConfigDict(from_attributes=True)


class CartsResponseModel(BaseModel):
    id: int = Field(..., description="ID of the cart")
    name: str = Field(..., description="Name of the cart")
    reminder_date: Optional[datetime] = Field(
        None, description="Reminder date of the cart"
    )
    status: CartStatus = Field(..., description="Status of the cart")

    model_config = ConfigDict(from_attributes=True)


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
