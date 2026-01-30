from abc import ABC, abstractmethod

class IEncryptPassword(ABC):
    @abstractmethod
    def encrypt_password(self, password: str) -> str:
        pass
    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pass
