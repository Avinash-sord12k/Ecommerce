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
    permissions: Optional[list[str]] = Field(
        None, description="List of permission names"
    )
    model_config = ConfigDict(from_attributes=True)


class RoleUpdateModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[list[str]] = None
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
