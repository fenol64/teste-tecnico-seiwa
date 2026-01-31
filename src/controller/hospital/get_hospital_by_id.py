from fastapi import HTTPException
import uuid
from src.domain.usecase.hospital.get_hospital_by_id import GetHospitalByIdUseCase


class GetHospitalByIdHandler:
    def __init__(self, get_hospital_by_id_usecase: GetHospitalByIdUseCase):
        self.get_hospital_by_id_usecase = get_hospital_by_id_usecase

    def handle(self, hospital_id: uuid.UUID):
        try:
            hospital = self.get_hospital_by_id_usecase.execute(hospital_id)
            return {
                "id": str(hospital.id),
                "name": hospital.name,
                "address": hospital.address,
                "created_at": hospital.created_at,
                "updated_at": hospital.updated_at
            }
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error while fetching hospital")
