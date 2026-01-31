from src.domain.usecase.interfaces.IGetHospitalsByDoctor import IGetHospitalsByDoctor
from typing import List
import uuid


class GetHospitalsByDoctorUseCase:
    def __init__(self, get_hospitals_by_doctor_port: IGetHospitalsByDoctor):
        self.get_hospitals_by_doctor_port = get_hospitals_by_doctor_port

    def execute(self, doctor_id: uuid.UUID) -> List[dict]:
        return self.get_hospitals_by_doctor_port.get_hospitals_by_doctor(doctor_id)
