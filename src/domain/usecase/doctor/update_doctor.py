from src.domain.usecase.interfaces.IUpdateDoctor import IUpdateDoctor
from src.domain.usecase.interfaces.IGetDoctorById import IGetDoctorById
from src.dto.doctorDTO import UpdateDoctorDTO
from typing import Optional
import uuid
from src.domain.entities.Doctor import Doctor


class UpdateDoctorUseCase:
    def __init__(
        self,
        update_doctor_port: IUpdateDoctor,
        get_doctor_by_id_port: IGetDoctorById
    ):
        self.update_doctor_port = update_doctor_port
        self.get_doctor_by_id_port = get_doctor_by_id_port

    def execute(self, doctor_id: uuid.UUID, doctor_data: UpdateDoctorDTO) -> Optional[Doctor]:
        # Verifica se o médico existe
        existing_doctor = self.get_doctor_by_id_port.get_by_id(doctor_id)
        if not existing_doctor:
            raise ValueError("Doctor not found.")

        # Prepara dados para atualização (apenas campos não nulos)
        update_data = {k: v for k, v in doctor_data.model_dump().items() if v is not None}

        if not update_data:
            return existing_doctor

        updated_doctor = self.update_doctor_port.update(doctor_id, **update_data)
        return updated_doctor
