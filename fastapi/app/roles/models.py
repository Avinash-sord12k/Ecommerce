from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models import PaginatedResponse


class RoleBase(BaseModel):
    """Base Role model with common fields and validations"""

    name: str = Field(
        ..., min_length=3, max_length=50, description="Name of the role"
    )
    description: str = Field(
        None, max_length=255, description="Description of the role"
    )
    model_config = ConfigDict(from_attributes=True)


class RoleCreateModel(RoleBase):
    pass


class RoleResponseModel(RoleBase):
    id: int = Field(..., description="ID of the role")
    permissions: Optional[list[str]] = Field(
        None, description="List of permission names"
    )


class RoleUpdateModel(BaseModel):
    name: Optional[str] = Field(
        None, min_length=3, max_length=50, description="Name of the role"
    )
    description: Optional[str] = Field(
        None, max_length=255, description="Description of the role"
    )
    permissions: Optional[list[str]] = Field(
        None, description="List of permission names"
    )
    model_config = ConfigDict(from_attributes=True)


class AllRolesResponseModel(PaginatedResponse):
    items: list[RoleResponseModel]
