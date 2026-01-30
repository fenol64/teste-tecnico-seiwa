from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Dict, Any

from src.infrastructure.database.connection import get_db
from src.infrastructure.services.jwt_service import JWTService


# Security scheme para o Swagger
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Dependency para validar o token JWT e retornar os dados do usuário atual.

    Uso:
        @router.get("/protected")
        async def protected_route(current_user: dict = Depends(get_current_user)):
            return {"user": current_user}

    Args:
        credentials: Credenciais HTTP Bearer (token JWT)
        db: Sessão do banco de dados

    Returns:
        Dados do usuário decodificados do token

    Raises:
        HTTPException: Se o token for inválido, expirado ou ausente
    """
    token = credentials.credentials
    token_service = JWTService()

    try:
        payload = token_service.verify_token(token)
        return payload
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user_id(current_user: Dict[str, Any] = Depends(get_current_user)) -> str:
    """
    Dependency para extrair apenas o ID do usuário atual.

    Uso:
        @router.get("/me")
        async def get_me(user_id: str = Depends(get_current_user_id)):
            return {"user_id": user_id}

    Args:
        current_user: Dados do usuário do token (obtidos via get_current_user)

    Returns:
        ID do usuário como string

    Raises:
        HTTPException: Se o token não contiver o ID do usuário
    """
    user_id = current_user.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    return user_id
