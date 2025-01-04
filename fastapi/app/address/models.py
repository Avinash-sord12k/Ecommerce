from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AddressBaseModel(BaseModel):
    name: str = Field(
        min_length=3, max_length=50, description="Name of the address"
    )
    address: str = Field(
        min_length=3, max_length=255, description="Address of the address"
    )
    city: str = Field(
        min_length=3, max_length=255, description="City of the address"
    )
    state: str = Field(
        min_length=3, max_length=255, description="State of the address"
    )
    country: str = Field(
        min_length=3, max_length=255, description="Country of the address"
    )
    pincode: str = Field(
        min_length=3, max_length=255, description="Pincode of the address"
    )

    model_config = ConfigDict(from_attributes=True)


class AddressCreateModel(AddressBaseModel):
    model_config = ConfigDict(from_attributes=True)


class AddressResponseModel(AddressBaseModel):
    id: int = Field(..., description="ID of the address")
    user_id: int = Field(..., description="ID of the user")
    model_config = ConfigDict(from_attributes=True)


class AddressUpdateModel(AddressBaseModel):
    id: int = Field(..., description="ID of the address")
    model_config = ConfigDict(from_attributes=True)


class AddressQueryParams(BaseModel):
    id: Optional[int] = Field(None, gt=0, description="ID of the address")
    name: Optional[str] = Field(
        None, min_length=3, max_length=50, description="Name of the address"
    )
    address: Optional[str] = Field(
        None,
        min_length=3,
        max_length=255,
        description="Address of the address",
    )
    city: Optional[str] = Field(
        None, min_length=3, max_length=255, description="City of the address"
    )
    state: Optional[str] = Field(
        None, min_length=3, max_length=255, description="State of the address"
    )
    country: Optional[str] = Field(
        None,
        min_length=3,
        max_length=255,
        description="Country of the address",
    )
    pincode: Optional[str] = Field(
        None,
        min_length=3,
        max_length=255,
        description="Pincode of the address",
    )

    model_config = ConfigDict(from_attributes=True)
