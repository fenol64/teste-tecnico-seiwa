import uuid
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class SignInDTO(BaseModel):
    """DTO para login de usuário"""
    email: EmailStr = Field(..., description="Email do usuário (deve ser válido)")
    password: str = Field(..., min_length=6, max_length=100, description="Senha do usuário (mínimo 6 caracteres)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "usuario@exemplo.com",
                "password": "senha123"
            }
        }
    )
