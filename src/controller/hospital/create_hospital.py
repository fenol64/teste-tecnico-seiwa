from fastapi import HTTPException
from src.dto.hospitalDTO import CreateHospitalDTO
from src.domain.usecase.hospital.create_hospital import CreateHospitalUseCase


import uuid

class CreateHospitalHandler:
    def __init__(self, create_hospital_usecase: CreateHospitalUseCase):
        self.create_hospital_usecase = create_hospital_usecase

    def handle(self, hospital_data: CreateHospitalDTO, user_id: str):
        try:
            hospital = self.create_hospital_usecase.execute(hospital_data, uuid.UUID(user_id))
            return {
                "id": str(hospital.id),
                "name": hospital.name,
                "address": hospital.address,
                "created_at": hospital.created_at,
                "updated_at": hospital.updated_at
            }
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error while creating hospital")
