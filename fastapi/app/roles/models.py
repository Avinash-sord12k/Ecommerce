from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RoleCreateModel(BaseModel):
    name: str = Field(
        ..., min_length=3, max_length=50, description="Name of the role"
    )
    description: str = Field(
        None, max_length=255, description="Description of the role"
    )
    model_config = ConfigDict(from_attributes=True)


class RoleResponseModel(BaseModel):
    id: int = Field(..., description="ID of the role")
    name: str = Field(
        ..., min_length=3, max_length=50, description="Name of the role"
    )
    description: str = Field(
        None, max_length=255, description="Description of the role"
    )
    permission_ids: Optional[list[int]] = Field(
        None, description="List of permission IDs"
    )
    model_config = ConfigDict(from_attributes=True)


class RoleUpdateModel(BaseModel):
    name: Optional[str] = Field(
        str,
        min_length=3,
        max_length=50,
        description="Name of the role",
    )
    description: Optional[str] = Field(
        None, max_length=255, description="Description of the role"
    )
    permission_ids: Optional[list[int]] = Field(
        None, description="List of permission IDs"
    )
    model_config = ConfigDict(from_attributes=True)


class AllRolesResponseModel(BaseModel):
    class MinimalRoleResponseModel(BaseModel):
        id: int = Field(..., description="ID of the role")
        name: str = Field(
            ..., min_length=3, max_length=50, description="Name of the role"
        )
        description: str = Field(
            None, max_length=255, description="Description of the role"
        )
        model_config = ConfigDict(from_attributes=True)

    roles: list[MinimalRoleResponseModel]
