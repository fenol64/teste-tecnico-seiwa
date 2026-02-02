from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
import uuid
from src.domain.entities.Production import Production


class IGetAllProductions(ABC):
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100, user_id: Optional[uuid.UUID] = None) -> Tuple[List[Production], int]:
        pass
