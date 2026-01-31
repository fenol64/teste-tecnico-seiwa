from fastapi import HTTPException
import uuid
from src.domain.usecase.doctor_hospital.get_doctors_by_hospital import GetDoctorsByHospitalUseCase


class GetDoctorsByHospitalHandler:
    def __init__(self, get_doctors_by_hospital_usecase: GetDoctorsByHospitalUseCase):
        self.get_doctors_by_hospital_usecase = get_doctors_by_hospital_usecase

    def handle(self, hospital_id: uuid.UUID):
        try:
            return self.get_doctors_by_hospital_usecase.execute(hospital_id)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error while fetching doctors by hospital")
