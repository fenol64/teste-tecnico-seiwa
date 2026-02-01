import uuid
from pydantic import BaseModel, Field, ConfigDict


class AssignDoctorToHospitalDTO(BaseModel):
    """DTO for assigning doctor to hospital"""
    doctor_id: str = Field(..., description="Doctor ID")
    hospital_id: str = Field(..., description="Hospital ID")

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
