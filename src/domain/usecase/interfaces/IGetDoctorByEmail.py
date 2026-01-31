from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.Doctor import Doctor


class IGetDoctorByEmail(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Doctor]:
        pass
