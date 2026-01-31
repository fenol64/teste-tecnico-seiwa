import uuid
from pydantic import BaseModel, Field
from datetime import date as date_type
from enum import Enum


class ProductionType(str, Enum):
    PLANTAO = "plantao"
    CONSULTA = "consulta"


class CreateProductionDTO(BaseModel):
    """DTO para criação de nova produção"""
    doctor_id: str = Field(..., description="ID do médico")
    type: ProductionType = Field(..., description="Tipo de produção (plantao ou consulta)")
    date: date_type = Field(..., description="Data da produção")
    description: str | None = Field(None, max_length=500, description="Descrição adicional (opcional)")

    class Config:
        json_schema_extra = {
            "example": {
                "doctor_id": "123e4567-e89b-12d3-a456-426614174000",
                "type": "plantao",
                "date": "2026-01-30",
                "description": "Plantão noturno no pronto socorro"
            }
        }


class UpdateProductionDTO(BaseModel):
    """DTO para atualização de produção"""
    type: ProductionType | None = Field(None, description="Tipo de produção (plantao ou consulta)")
    date: date_type | None = Field(None, description="Data da produção")
    description: str | None = Field(None, max_length=500, description="Descrição adicional")

    class Config:
        json_schema_extra = {
            "example": {
                "type": "consulta",
                "date": "2026-01-31",
                "description": "Consulta de rotina"
            }
        }


class ProductionResponseDTO(BaseModel):
    """DTO de resposta com dados da produção"""
    id: str
    doctor_id: str
    type: str
    date: str
    description: str | None = None
    created_at: str
    updated_at: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "doctor_id": "987e6543-e21b-12d3-a456-426614174999",
                "type": "plantao",
                "date": "2026-01-30",
                "description": "Plantão noturno no pronto socorro",
                "created_at": "2026-01-30T10:00:00",
                "updated_at": None
            }
        }
