from abc import ABC, abstractmethod
from typing import Optional
import uuid
from src.domain.entities.Hospital import Hospital


class IGetHospitalById(ABC):
    @abstractmethod
    def get_by_id(self, hospital_id: uuid.UUID) -> Optional[Hospital]:
        pass
