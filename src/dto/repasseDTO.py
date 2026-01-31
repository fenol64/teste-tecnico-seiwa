from pydantic import BaseModel, Field
from decimal import Decimal
from uuid import UUID
from datetime import datetime
from typing import Optional
from src.domain.enums.repasse_status import RepasseStatus


class CreateRepasseDTO(BaseModel):
    production_id: UUID = Field(..., description="ID da produção", example="123e4567-e89b-12d3-a456-426614174000")
    valor: Decimal = Field(..., gt=0, description="Valor do repasse", example=1500.00)
    status: Optional[RepasseStatus] = Field(default=RepasseStatus.PENDENTE, description="Status do repasse")

    model_config = {
        "json_schema_extra": {
            "example": {
                "production_id": "123e4567-e89b-12d3-a456-426614174000",
                "valor": 1500.00,
                "status": "pendente"
            }
        }
    }


class UpdateRepasseDTO(BaseModel):
    valor: Optional[Decimal] = Field(None, gt=0, description="Valor do repasse", example=1800.00)
    status: Optional[RepasseStatus] = Field(None, description="Status do repasse", example="consolidado")

    model_config = {
        "json_schema_extra": {
            "example": {
                "valor": 1800.00,
                "status": "consolidado"
            }
        }
    }


class RepasseResponseDTO(BaseModel):
    id: UUID
    production_id: UUID
    valor: Decimal
    status: RepasseStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "production_id": "123e4567-e89b-12d3-a456-426614174001",
                "valor": 1500.00,
                "status": "pendente",
                "created_at": "2024-01-01T10:00:00",
                "updated_at": "2024-01-01T10:00:00"
            }
        }
    }


class RepasseStatsDTO(BaseModel):
    doctor_id: UUID
    periodo_inicio: Optional[datetime]
    periodo_fim: Optional[datetime]
    total_pendente_qtd: int
    total_pendente_valor: Decimal
    total_consolidado_qtd: int
    total_consolidado_valor: Decimal
