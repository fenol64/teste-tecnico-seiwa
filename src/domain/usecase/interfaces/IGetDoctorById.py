from abc import ABC, abstractmethod
from typing import Optional
import uuid
from src.domain.entities.Doctor import Doctor


class IGetDoctorById(ABC):
    @abstractmethod
    def get_by_id(self, doctor_id: uuid.UUID) -> Optional[Doctor]:
        pass
