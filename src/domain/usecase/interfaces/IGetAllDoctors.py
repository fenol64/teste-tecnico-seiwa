from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
import uuid
from src.domain.entities.Doctor import Doctor


class IGetAllDoctors(ABC):
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100, user_id: Optional[uuid.UUID] = None) -> Tuple[List[Doctor], int]:
        pass
