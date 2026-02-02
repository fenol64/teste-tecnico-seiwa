from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from uuid import UUID
from datetime import datetime
from src.domain.entities.Repasse import Repasse
from src.dto.repasseDTO import CreateRepasseDTO, UpdateRepasseDTO


class IRepasseRepository(ABC):
    @abstractmethod
    def create(self, data: CreateRepasseDTO, user_id: UUID) -> Repasse:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100, user_id: Optional[UUID] = None) -> Tuple[List[Repasse], int]:
        pass

    @abstractmethod
    def get_by_doctor_and_date_range(
        self,
        doctor_id: UUID,
        start_date: Optional[datetime],
        end_date: Optional[datetime]
    ) -> List[Repasse]:
        pass

    @abstractmethod
    def get_by_id(self, repasse_id: UUID) -> Optional[Repasse]:
        pass

    @abstractmethod
    def get_by_hospital(self, hospital_id: UUID) -> List[Repasse]:
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
