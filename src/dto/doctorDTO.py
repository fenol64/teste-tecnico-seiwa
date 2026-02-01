import uuid
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class CreateDoctorDTO(BaseModel):
    """DTO for creating a new doctor"""
    name: str = Field(..., min_length=3, max_length=100, description="Doctor's full name")
    crm: str = Field(..., min_length=4, max_length=20, description="Doctor's CRM number")
    specialty: str = Field(..., min_length=3, max_length=100, description="Medical specialty")
    phone: str | None = Field(None, max_length=20, description="Doctor's phone (optional)")
    email: EmailStr = Field(..., description="Doctor's email (must be valid)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Dr. Carlos Mendes",
                "crm": "123456",
                "specialty": "Cardiology",
                "phone": "(11) 98765-4321",
                "email": "carlos.mendes@hospital.com"
            }
        }
    )


class UpdateDoctorDTO(BaseModel):
    """DTO for updating a doctor"""
    name: str | None = Field(None, min_length=3, max_length=100, description="Doctor's full name")
    specialty: str | None = Field(None, min_length=3, max_length=100, description="Medical specialty")
    phone: str | None = Field(None, max_length=20, description="Doctor's phone")
    email: EmailStr | None = Field(None, description="Doctor's email")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Dr. Carlos Mendes",
                "specialty": "Cardiology",
                "phone": "(11) 98765-4321",
                "email": "carlos.mendes@hospital.com"
            }
        }
    )


class DoctorResponseDTO(BaseModel):
    """Response DTO with doctor data"""
    id: str
    name: str
    crm: str
    specialty: str
    phone: str | None = None
    email: str
    created_at: str
    updated_at: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Dr. Carlos Mendes",
                "crm": "123456",
                "specialty": "Cardiologia",
                "phone": "(11) 98765-4321",
                "email": "carlos.mendes@hospital.com",
                "created_at": "2026-01-30T10:00:00",
                "updated_at": None
            }
        }
    )
