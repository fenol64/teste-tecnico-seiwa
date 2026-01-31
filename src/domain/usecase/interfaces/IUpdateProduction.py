from abc import ABC, abstractmethod
from typing import Optional
import uuid
from src.domain.entities.Production import Production


class IUpdateProduction(ABC):
    @abstractmethod
    def update(self, production_id: uuid.UUID, **kwargs) -> Optional[Production]:
        pass
