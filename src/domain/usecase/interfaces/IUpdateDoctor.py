from abc import ABC, abstractmethod
from typing import Optional
import uuid
from src.domain.entities.Doctor import Doctor


class IUpdateDoctor(ABC):
    @abstractmethod
    def update(self, doctor_id: uuid.UUID, **kwargs) -> Optional[Doctor]:
        pass
