import uuid
from pydantic import BaseModel, Field, ConfigDict


class AssignDoctorToHospitalDTO(BaseModel):
    """DTO para vincular médico a hospital"""
    doctor_id: str = Field(..., description="ID do médico")
    hospital_id: str = Field(..., description="ID do hospital")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "doctor_id": "123e4567-e89b-12d3-a456-426614174000",
                "hospital_id": "987e6543-e21b-12d3-a456-426614174999"
            }
        }
    )


class DoctorHospitalResponseDTO(BaseModel):
    """DTO de resposta da relação médico-hospital"""
    doctor_id: str
    hospital_id: str
    created_at: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "doctor_id": "123e4567-e89b-12d3-a456-426614174000",
                "hospital_id": "987e6543-e21b-12d3-a456-426614174999",
                "created_at": "2026-01-30T10:00:00"
            }
        }
    )
