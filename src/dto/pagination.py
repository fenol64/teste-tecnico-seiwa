from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field, ConfigDict
import math

T = TypeVar('T')

class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(default=1, ge=1, description="Page number (starts at 1)")
    page_size: int = Field(default=10, ge=1, le=100, description="Items per page")

    model_config = ConfigDict(from_attributes=True)

    @property
    def skip(self) -> int:
        """Calculates offset based on page"""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """Returns item limit"""
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response"""
    items: List[T]
    total: int = Field(description="Total items available")
    page: int = Field(description="Current page")
    page_size: int = Field(description="Items per page")
    total_pages: int = Field(description="Total pages")

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def create(cls, items: List[T], total: int, page: int, page_size: int):
        """Factory method to create paginated response"""
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=math.ceil(total / page_size) if page_size > 0 else 0
        )
