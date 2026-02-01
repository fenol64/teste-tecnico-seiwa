from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from src.domain.entities.Production import Production

class IGetProductionsByHospital(ABC):
    @abstractmethod
    def get_by_hospital(self, hospital_id: UUID) -> List[Production]:
        pass
