from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.Doctor import Doctor


class IGetDoctorByCRM(ABC):
    @abstractmethod
    def get_by_crm(self, crm: str) -> Optional[Doctor]:
        pass
