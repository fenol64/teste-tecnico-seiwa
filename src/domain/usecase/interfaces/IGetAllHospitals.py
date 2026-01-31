from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.Hospital import Hospital


class IGetAllHospitals(ABC):
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Hospital]:
        pass
