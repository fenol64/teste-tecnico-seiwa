from fastapi import HTTPException
import uuid
from src.domain.usecase.doctor_hospital.assign_doctor_to_hospital import AssignDoctorToHospitalUseCase


class AssignDoctorToHospitalHandler:
    def __init__(self, assign_doctor_to_hospital_usecase: AssignDoctorToHospitalUseCase):
        self.assign_doctor_to_hospital_usecase = assign_doctor_to_hospital_usecase

    def handle(self, doctor_id: uuid.UUID, hospital_id: uuid.UUID):
        try:
            result = self.assign_doctor_to_hospital_usecase.execute(doctor_id, hospital_id)
            return result
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error while assigning doctor to hospital")
