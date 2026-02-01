from abc import ABC, abstractmethod
from typing import List, Tuple
from src.domain.entities.Production import Production


class IGetAllProductions(ABC):
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> Tuple[List[Production], int]:
        pass
