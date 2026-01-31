from src.domain.usecase.interfaces.IGetProductionsByDoctor import IGetProductionsByDoctor
from typing import List
import uuid
from src.domain.entities.Production import Production


class GetProductionsByDoctorUseCase:
    def __init__(self, get_productions_by_doctor_port: IGetProductionsByDoctor):
        self.get_productions_by_doctor_port = get_productions_by_doctor_port

    def execute(self, doctor_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Production]:
        return self.get_productions_by_doctor_port.get_by_doctor(doctor_id, skip=skip, limit=limit)
