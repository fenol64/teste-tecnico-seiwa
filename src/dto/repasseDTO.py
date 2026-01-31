from pydantic import BaseModel, Field
from decimal import Decimal
from uuid import UUID
from datetime import datetime


class CreateRepasseDTO(BaseModel):
    production_id: UUID = Field(..., description="ID da produção", example="123e4567-e89b-12d3-a456-426614174000")
    valor: Decimal = Field(..., gt=0, description="Valor do repasse", example=1500.00)

    model_config = {
        "json_schema_extra": {
            "example": {
                "production_id": "123e4567-e89b-12d3-a456-426614174000",
                "valor": 1500.00
            }
        }
    }


class UpdateRepasseDTO(BaseModel):
    valor: Decimal = Field(..., gt=0, description="Valor do repasse", example=1800.00)

    model_config = {
        "json_schema_extra": {
            "example": {
                "valor": 1800.00
            }
        }
    }


class RepasseResponseDTO(BaseModel):
    id: UUID
    production_id: UUID
    valor: Decimal
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "production_id": "123e4567-e89b-12d3-a456-426614174001",
                "valor": 1500.00,
                "created_at": "2024-01-01T10:00:00",
                "updated_at": "2024-01-01T10:00:00"
            }
        }
    }
