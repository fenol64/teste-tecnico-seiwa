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
