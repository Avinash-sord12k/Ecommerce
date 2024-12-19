from typing import Generic, TypeVar

from pydantic import BaseModel, Field, computed_field, field_validator

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = Field(default=1, gt=0, description="Page number")
    page_size: int = Field(
        default=10, gt=0, le=100, description="Items per page"
    )


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    @computed_field
    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @computed_field
    @property
    def has_previous(self) -> bool:
        return self.page > 1

    @field_validator("page", "page_size", "total", mode="before")
    def validate_positive(cls, value: int) -> int:
        if value < 1:
            raise ValueError("Value must be greater than 0")
        return value
