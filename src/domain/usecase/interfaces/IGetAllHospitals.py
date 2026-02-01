from abc import ABC, abstractmethod
from typing import List, Tuple
from src.domain.entities.Hospital import Hospital


class IGetAllHospitals(ABC):
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> Tuple[List[Hospital], int]:
        pass
