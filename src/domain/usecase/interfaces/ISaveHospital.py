from abc import ABC, abstractmethod
from src.domain.entities.Hospital import Hospital


class ISaveHospital(ABC):
    @abstractmethod
    def save(self, hospital: Hospital) -> Hospital:
        pass
