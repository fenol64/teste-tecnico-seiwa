from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from src.domain.entities.Repasse import Repasse
from src.dto.repasseDTO import CreateRepasseDTO, UpdateRepasseDTO


class IRepasseRepository(ABC):
    @abstractmethod
    def create(self, data: CreateRepasseDTO) -> Repasse:
        pass

    @abstractmethod
    def get_all(self) -> List[Repasse]:
        pass

    @abstractmethod
    def get_by_id(self, repasse_id: UUID) -> Optional[Repasse]:
        pass

    @abstractmethod
    def update(self, repasse_id: UUID, data: UpdateRepasseDTO) -> Optional[Repasse]:
        pass

    @abstractmethod
    def delete(self, repasse_id: UUID) -> bool:
        pass

    @abstractmethod
    def get_by_production(self, production_id: UUID) -> List[Repasse]:
        pass
