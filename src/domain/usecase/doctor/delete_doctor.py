from src.domain.usecase.interfaces.IDeleteDoctor import IDeleteDoctor
from src.domain.usecase.interfaces.IGetDoctorById import IGetDoctorById
import uuid


class DeleteDoctorUseCase:
    def __init__(
        self,
        delete_doctor_port: IDeleteDoctor,
        get_doctor_by_id_port: IGetDoctorById
    ):
        self.delete_doctor_port = delete_doctor_port
        self.get_doctor_by_id_port = get_doctor_by_id_port

    def execute(self, doctor_id: uuid.UUID) -> bool:
        # Verifica se o médico existe
        existing_doctor = self.get_doctor_by_id_port.get_by_id(doctor_id)
        if not existing_doctor:
            raise ValueError("Doctor not found.")

        return self.delete_doctor_port.delete(doctor_id)
