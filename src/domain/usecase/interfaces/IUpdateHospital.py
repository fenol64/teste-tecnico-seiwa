from abc import ABC, abstractmethod
from typing import Optional
import uuid
from src.domain.entities.Hospital import Hospital


class IUpdateHospital(ABC):
    @abstractmethod
    def update(self, hospital_id: uuid.UUID, **kwargs) -> Optional[Hospital]:
        pass
