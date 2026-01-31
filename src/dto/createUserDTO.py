import uuid
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class CreateUserDTO(BaseModel):
    """DTO para criação de novo usuário"""
    name: str = Field(..., min_length=3, max_length=100, description="Nome completo do usuário")
    email: EmailStr = Field(..., description="Email do usuário (deve ser válido)")
    password: str = Field(..., min_length=6, max_length=100, description="Senha do usuário (mínimo 6 caracteres)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "João Silva",
                "email": "joao.silva@exemplo.com",
                "password": "senha123"
            }
        }
    )