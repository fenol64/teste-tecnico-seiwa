from abc import ABC, abstractmethod
from typing import List
import uuid
from src.domain.entities.Production import Production


class IGetProductionsByDoctor(ABC):
    @abstractmethod
    def get_by_doctor(self, doctor_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Production]:
        pass
