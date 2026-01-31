from src.domain.usecase.interfaces.IGetDoctorsByHospital import IGetDoctorsByHospital
from typing import List
import uuid


class GetDoctorsByHospitalUseCase:
    def __init__(self, get_doctors_by_hospital_port: IGetDoctorsByHospital):
        self.get_doctors_by_hospital_port = get_doctors_by_hospital_port

    def execute(self, hospital_id: uuid.UUID) -> List[dict]:
        return self.get_doctors_by_hospital_port.get_doctors_by_hospital(hospital_id)
