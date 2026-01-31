from src.domain.usecase.interfaces.IRemoveDoctorFromHospital import IRemoveDoctorFromHospital
import uuid


class RemoveDoctorFromHospitalUseCase:
    def __init__(self, remove_doctor_from_hospital_port: IRemoveDoctorFromHospital):
        self.remove_doctor_from_hospital_port = remove_doctor_from_hospital_port

    def execute(self, doctor_id: uuid.UUID, hospital_id: uuid.UUID) -> bool:
        result = self.remove_doctor_from_hospital_port.remove_doctor_from_hospital(doctor_id, hospital_id)
        if not result:
            raise ValueError("Doctor-Hospital relationship not found.")
        return result
