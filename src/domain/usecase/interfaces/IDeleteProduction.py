from abc import ABC, abstractmethod
import uuid


class IDeleteProduction(ABC):
    @abstractmethod
    def delete(self, production_id: uuid.UUID) -> bool:
        pass
