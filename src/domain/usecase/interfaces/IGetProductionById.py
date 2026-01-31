from abc import ABC, abstractmethod
from typing import Optional
import uuid
from src.domain.entities.Production import Production


class IGetProductionById(ABC):
    @abstractmethod
    def get_by_id(self, production_id: uuid.UUID) -> Optional[Production]:
        pass
