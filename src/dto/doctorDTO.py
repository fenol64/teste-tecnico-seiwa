import uuid
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class CreateDoctorDTO(BaseModel):
    """DTO para criação de novo médico"""
    name: str = Field(..., min_length=3, max_length=100, description="Nome completo do médico")
    crm: str = Field(..., min_length=4, max_length=20, description="Número do CRM do médico")
    specialty: str = Field(..., min_length=3, max_length=100, description="Especialidade médica")
    phone: str | None = Field(None, max_length=20, description="Telefone do médico (opcional)")
    email: EmailStr = Field(..., description="Email do médico (deve ser válido)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Dr. Carlos Mendes",
                "crm": "123456",
                "specialty": "Cardiologia",
                "phone": "(11) 98765-4321",
                "email": "carlos.mendes@hospital.com"
            }
        }
    )


class UpdateDoctorDTO(BaseModel):
    """DTO para atualização de médico"""
    name: str | None = Field(None, min_length=3, max_length=100, description="Nome completo do médico")
    specialty: str | None = Field(None, min_length=3, max_length=100, description="Especialidade médica")
    phone: str | None = Field(None, max_length=20, description="Telefone do médico")
    email: EmailStr | None = Field(None, description="Email do médico")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Dr. Carlos Mendes",
                "specialty": "Cardiologia",
                "phone": "(11) 98765-4321",
                "email": "carlos.mendes@hospital.com"
            }
        }
    )


class DoctorResponseDTO(BaseModel):
    """DTO de resposta com dados do médico"""
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
