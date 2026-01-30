from fastapi import APIRouter, Depends, status
from typing import Dict, Any

from src.infrastructure.auth.dependencies import get_current_user, get_current_user_id
from src.dto.responses import UserData

router = APIRouter()


@router.get(
    "/me",
    summary="Obter Dados do Usuário Atual",
    description="Retorna os dados do usuário autenticado (rota protegida)",
    response_model=UserData,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Dados do usuário retornados com sucesso",
            "model": UserData
        },
        401: {
            "description": "Token inválido ou ausente",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid authentication credentials"}
                }
            }
        }
    }
)
async def get_me(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Rota protegida que retorna os dados do usuário autenticado.

    Requer um token JWT válido no header Authorization: Bearer <token>

    O token é obtido após fazer login com sucesso na rota /api/v1/signin
    """
    return {
        "id": current_user.get("sub"),
        "name": current_user.get("name"),
        "email": current_user.get("email")
    }
