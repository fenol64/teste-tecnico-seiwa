from abc import ABC, abstractmethod
from typing import Dict, Any


class ITokenService(ABC):
    @abstractmethod
    def create_access_token(self, data: Dict[str, Any], expires_delta: int = None) -> str:
        """
        Cria um token de acesso JWT.

        Args:
            data: Dados a serem codificados no token
            expires_delta: Tempo de expiração em minutos (opcional)

        Returns:
            Token JWT como string
        """
        pass

    @abstractmethod
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
        pass
