from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field, ConfigDict
import math

T = TypeVar('T')

class PaginationParams(BaseModel):
    """Parâmetros de paginação"""
    page: int = Field(default=1, ge=1, description="Número da página (começa em 1)")
    page_size: int = Field(default=10, ge=1, le=100, description="Quantidade de itens por página")

    model_config = ConfigDict(from_attributes=True)

    @property
    def skip(self) -> int:
        """Calcula o offset baseado na página"""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """Retorna o limite de itens"""
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Resposta paginada genérica"""
    items: List[T]
    total: int = Field(description="Total de itens disponíveis")
    page: int = Field(description="Página atual")
    page_size: int = Field(description="Itens por página")
    total_pages: int = Field(description="Total de páginas")

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def create(cls, items: List[T], total: int, page: int, page_size: int):
        """Factory method para criar resposta paginada"""
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=math.ceil(total / page_size) if page_size > 0 else 0
        )
