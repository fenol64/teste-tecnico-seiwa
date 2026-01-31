from abc import ABC, abstractmethod
from src.domain.entities.Production import Production


class ISaveProduction(ABC):
    @abstractmethod
    def save(self, production: Production) -> Production:
        pass
