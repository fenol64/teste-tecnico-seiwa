from typing import List
from uuid import UUID
from src.domain.entities.Repasse import Repasse
from src.domain.usecase.interfaces.repasse_repository_interface import IRepasseRepository

class GetRepassesByHospitalUseCase:
    def __init__(self, repasse_repository: IRepasseRepository):
        self.repasse_repository = repasse_repository

    def execute(self, hospital_id: UUID) -> List[Repasse]:
        return self.repasse_repository.get_by_hospital(hospital_id)
