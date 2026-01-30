from abc import ABC, abstractmethod
from src.domain.entities.User import User

class ISaveUser(ABC):
    @abstractmethod
    def save_user(self, user: User) -> None:
        pass
