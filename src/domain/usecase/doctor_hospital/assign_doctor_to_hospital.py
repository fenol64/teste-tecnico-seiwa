from src.domain.usecase.interfaces.IAssignDoctorToHospital import IAssignDoctorToHospital
from src.domain.usecase.interfaces.IGetDoctorById import IGetDoctorById
from src.domain.usecase.interfaces.IGetHospitalById import IGetHospitalById
import uuid


class AssignDoctorToHospitalUseCase:
    def __init__(
        self,
        assign_doctor_to_hospital_port: IAssignDoctorToHospital,
        get_doctor_by_id_port: IGetDoctorById,
        get_hospital_by_id_port: IGetHospitalById
    ):
        self.assign_doctor_to_hospital_port = assign_doctor_to_hospital_port
        self.get_doctor_by_id_port = get_doctor_by_id_port
        self.get_hospital_by_id_port = get_hospital_by_id_port

    def execute(self, doctor_id: uuid.UUID, hospital_id: uuid.UUID) -> dict:
        # Verifica se o médico existe
        doctor = self.get_doctor_by_id_port.get_by_id(doctor_id)
        if not doctor:
            raise ValueError("Doctor not found.")

        # Verifica se o hospital existe
        hospital = self.get_hospital_by_id_port.get_by_id(hospital_id)
        if not hospital:
            raise ValueError("Hospital not found.")

        return self.assign_doctor_to_hospital_port.assign_doctor_to_hospital(doctor_id, hospital_id)
