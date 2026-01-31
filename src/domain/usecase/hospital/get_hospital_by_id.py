from src.domain.usecase.interfaces.IGetHospitalById import IGetHospitalById
from typing import Optional
import uuid
from src.domain.entities.Hospital import Hospital


class GetHospitalByIdUseCase:
    def __init__(self, get_hospital_by_id_port: IGetHospitalById):
        self.get_hospital_by_id_port = get_hospital_by_id_port

    def execute(self, hospital_id: uuid.UUID) -> Optional[Hospital]:
        hospital = self.get_hospital_by_id_port.get_by_id(hospital_id)
        if not hospital:
            raise ValueError("Hospital not found.")
        return hospital
