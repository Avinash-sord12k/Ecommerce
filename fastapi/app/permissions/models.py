from pydantic import BaseModel, ConfigDict, Field


class PermissionCreateModel(BaseModel):
    name: str = Field(
        ..., min_length=3, max_length=50, description="Name of the permission"
    )
    description: str = Field(
        None, max_length=255, description="Description of the permission"
    )
    model_config = ConfigDict(from_attributes=True)


class PermissionResponseModel(BaseModel):
    id: int = Field(..., description="ID of the permission")
    name: str = Field(
        ..., min_length=3, max_length=50, description="Name of the permission"
    )
    description: str = Field(
        None, max_length=255, description="Description of the permission"
    )
    model_config = ConfigDict(from_attributes=True)


class AllPermissionsResponseModel(BaseModel):
    permissions: list[PermissionResponseModel]
