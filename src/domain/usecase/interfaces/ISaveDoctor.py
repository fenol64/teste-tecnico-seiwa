from abc import ABC, abstractmethod
from src.domain.entities.Doctor import Doctor


class ISaveDoctor(ABC):
    @abstractmethod
    def save(self, doctor: Doctor) -> Doctor:
        pass
