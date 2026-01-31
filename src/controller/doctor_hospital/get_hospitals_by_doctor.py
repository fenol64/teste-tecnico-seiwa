from fastapi import HTTPException
import uuid
from src.domain.usecase.doctor_hospital.get_hospitals_by_doctor import GetHospitalsByDoctorUseCase


class GetHospitalsByDoctorHandler:
    def __init__(self, get_hospitals_by_doctor_usecase: GetHospitalsByDoctorUseCase):
        self.get_hospitals_by_doctor_usecase = get_hospitals_by_doctor_usecase

    def handle(self, doctor_id: uuid.UUID):
        try:
            return self.get_hospitals_by_doctor_usecase.execute(doctor_id)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error while fetching hospitals by doctor")
