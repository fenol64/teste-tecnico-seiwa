import uuid
from pydantic import BaseModel, Field, ConfigDict


class CreateHospitalDTO(BaseModel):
    """DTO for creating a new hospital"""
    name: str = Field(..., min_length=3, max_length=200, description="Hospital name")
    address: str = Field(..., min_length=5, max_length=300, description="Hospital full address")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "General Hospital",
                "address": "123 Flower St, City, State"
            }
        }
    )


class UpdateHospitalDTO(BaseModel):
    """DTO for updating a hospital"""
    name: str | None = Field(None, min_length=3, max_length=200, description="Hospital name")
    address: str | None = Field(None, min_length=5, max_length=300, description="Hospital full address")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "General Hospital",
                "address": "123 Flower St, City, State"
            }
        }
    )


class HospitalResponseDTO(BaseModel):
    """Response DTO with hospital data"""
    id: str
    name: str
    address: str
    created_at: str
    updated_at: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "General Hospital",
                "address": "123 Flower St, City, State",
                "created_at": "2026-01-30T10:00:00",
                "updated_at": None
            }
        }
    )
