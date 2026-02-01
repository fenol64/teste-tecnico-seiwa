from typing import List
from uuid import UUID
from src.domain.entities.Production import Production
from src.domain.usecase.interfaces.IGetProductionsByHospital import IGetProductionsByHospital

class GetProductionsByHospitalUseCase:
    def __init__(self, repository: IGetProductionsByHospital):
        self.repository = repository

    def execute(self, hospital_id: UUID) -> List[Production]:
        return self.repository.get_by_hospital(hospital_id)
