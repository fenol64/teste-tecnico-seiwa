from abc import ABC, abstractmethod
import uuid


class IDeleteDoctor(ABC):
    @abstractmethod
    def delete(self, doctor_id: uuid.UUID) -> bool:
        pass
