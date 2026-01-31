from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.Doctor import Doctor


class IGetAllDoctors(ABC):
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Doctor]:
        pass
