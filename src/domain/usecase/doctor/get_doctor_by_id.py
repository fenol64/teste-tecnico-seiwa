from src.domain.usecase.interfaces.IGetDoctorById import IGetDoctorById
from typing import Optional
import uuid
from src.domain.entities.Doctor import Doctor


class GetDoctorByIdUseCase:
    def __init__(self, get_doctor_by_id_port: IGetDoctorById):
        self.get_doctor_by_id_port = get_doctor_by_id_port

    def execute(self, doctor_id: uuid.UUID) -> Optional[Doctor]:
        doctor = self.get_doctor_by_id_port.get_by_id(doctor_id)
        if not doctor:
            raise ValueError("Doctor not found.")
        return doctor
