from abc import ABC, abstractmethod
from src.domain.entities.User import User

class IGetUserByEmail(ABC):
    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        pass
