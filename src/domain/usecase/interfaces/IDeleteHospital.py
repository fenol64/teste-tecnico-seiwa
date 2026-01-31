from abc import ABC, abstractmethod
import uuid


class IDeleteHospital(ABC):
    @abstractmethod
    def delete(self, hospital_id: uuid.UUID) -> bool:
        pass
