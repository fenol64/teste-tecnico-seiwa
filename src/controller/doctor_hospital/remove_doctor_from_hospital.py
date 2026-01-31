from fastapi import HTTPException
import uuid
from src.domain.usecase.doctor_hospital.remove_doctor_from_hospital import RemoveDoctorFromHospitalUseCase


class RemoveDoctorFromHospitalHandler:
    def __init__(self, remove_doctor_from_hospital_usecase: RemoveDoctorFromHospitalUseCase):
        self.remove_doctor_from_hospital_usecase = remove_doctor_from_hospital_usecase

    def handle(self, doctor_id: uuid.UUID, hospital_id: uuid.UUID):
        try:
            self.remove_doctor_from_hospital_usecase.execute(doctor_id, hospital_id)
            return {"message": "Doctor removed from hospital successfully"}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error while removing doctor from hospital")
