from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    """Resposta padrão de sucesso"""
    message: str = Field(..., description="Mensagem de sucesso")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operação realizada com sucesso"
            }
        }


class SignUpResponse(BaseModel):
    """Resposta do cadastro de usuário"""
    message: str = Field(..., description="Mensagem de confirmação")
    email: str = Field(..., description="Email do usuário cadastrado")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Usuário cadastrado com sucesso!",
                "email": "usuario@exemplo.com"
            }
        }


class ErrorResponse(BaseModel):
    """Resposta padrão de erro"""
    detail: str = Field(..., description="Detalhes do erro")

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Erro ao processar a requisição"
            }
        }


class HealthCheckResponse(BaseModel):
    """Resposta do health check"""
    status: str = Field(..., description="Status da aplicação")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "ok"
            }
        }


class UserData(BaseModel):
    """Dados do usuário"""
    id: str = Field(..., description="ID único do usuário")
    name: str = Field(..., description="Nome do usuário")
    email: str = Field(..., description="Email do usuário")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "João Silva",
                "email": "joao.silva@exemplo.com"
            }
        }


class SignInResponse(BaseModel):
    """Resposta do login de usuário"""
    message: str = Field(..., description="Mensagem de confirmação")
    access_token: str = Field(..., description="Token JWT de acesso")
    token_type: str = Field(default="bearer", description="Tipo do token")
    user: UserData = Field(..., description="Dados do usuário autenticado")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Login successful",
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "João Silva",
                    "email": "joao.silva@exemplo.com"
                }
            }
        }


class DeleteResponseDTO(BaseModel):
    """Resposta padrão de deleção"""
    message: str = Field(..., description="Mensagem de confirmação da deleção")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Registro deletado com sucesso"
            }
        }
