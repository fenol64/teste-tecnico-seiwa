from datetime import datetime, timedelta, timezone
from typing import Dict, Any
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

from src.domain.usecase.interfaces.ITokenService import ITokenService

load_dotenv()


class JWTService(ITokenService):
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
        self.algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        self.access_token_expire_minutes = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    def create_access_token(self, data: Dict[str, Any], expires_delta: int = None) -> str:
        """
        Cria um token de acesso JWT.

        Args:
            data: Dados a serem codificados no token (ex: {"sub": user_id, "email": email})
            expires_delta: Tempo de expiração em minutos (opcional, usa padrão se None)

        Returns:
            Token JWT como string
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

        return encoded_jwt

    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verifica e decodifica um token JWT.

        Args:
            token: Token JWT a ser verificado

        Returns:
            Dados decodificados do token

        Raises:
            ValueError: Se o token for inválido ou expirado
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError as e:
            raise ValueError(f"Invalid token: {str(e)}")
