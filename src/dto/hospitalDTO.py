import uuid
from pydantic import BaseModel, Field


class CreateHospitalDTO(BaseModel):
    """DTO para criação de novo hospital"""
    name: str = Field(..., min_length=3, max_length=200, description="Nome do hospital")
    address: str = Field(..., min_length=5, max_length=300, description="Endereço completo do hospital")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Hospital Santa Casa",
                "address": "Rua das Flores, 123 - Centro, São Paulo - SP"
            }
        }


class UpdateHospitalDTO(BaseModel):
    """DTO para atualização de hospital"""
    name: str | None = Field(None, min_length=3, max_length=200, description="Nome do hospital")
    address: str | None = Field(None, min_length=5, max_length=300, description="Endereço completo do hospital")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Hospital Santa Casa",
                "address": "Rua das Flores, 123 - Centro, São Paulo - SP"
            }
        }


class HospitalResponseDTO(BaseModel):
    """DTO de resposta com dados do hospital"""
    id: str
    name: str
    address: str
    created_at: str
    updated_at: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Hospital Santa Casa",
                "address": "Rua das Flores, 123 - Centro, São Paulo - SP",
                "created_at": "2026-01-30T10:00:00",
                "updated_at": None
            }
        }
