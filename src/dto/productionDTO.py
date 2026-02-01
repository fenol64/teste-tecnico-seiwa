import uuid
from pydantic import BaseModel, Field, ConfigDict
from datetime import date as date_type
from enum import Enum


class ProductionType(str, Enum):
    SHIFT = "shift"
    CONSULTATION = "consultation"


class CreateProductionDTO(BaseModel):
    """DTO for creating a new production"""
    doctor_id: str = Field(..., description="Doctor ID")
    hospital_id: str = Field(..., description="Hospital ID")
    type: ProductionType = Field(..., description="Production type (shift or consultation)")
    date: date_type = Field(..., description="Production date")
    description: str | None = Field(None, max_length=500, description="Additional description (optional)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "doctor_id": "123e4567-e89b-12d3-a456-426614174000",
                "hospital_id": "987e6543-e21b-12d3-a456-426614174999",
                "type": "shift",
                "date": "2026-01-30",
                "description": "Night shift at ER"
            }
        }
    )


class UpdateProductionDTO(BaseModel):
    """DTO for updating a production"""
    type: ProductionType | None = Field(None, description="Production type (shift or consultation)")
    date: date_type | None = Field(None, description="Production date")
    description: str | None = Field(None, max_length=500, description="Additional description")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "consultation",
                "date": "2026-01-31",
                "description": "Routine consultation"
            }
        }
    )


class ProductionResponseDTO(BaseModel):
    """DTO for production response data"""
    id: str
    doctor_id: str
    hospital_id: str
    type: str
    date: str
    description: str | None = None
    created_at: str
    updated_at: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "doctor_id": "987e6543-e21b-12d3-a456-426614174999",
                "hospital_id": "456e7890-a12b-34c5-d678-901234567890",
                "type": "shift",
                "date": "2026-01-30",
                "description": "Night shift at ER",
                "created_at": "2026-01-30T10:00:00",
                "updated_at": None
            }
        }
    )
