from fastapi import HTTPException
import uuid
from src.dto.hospitalDTO import UpdateHospitalDTO
from src.domain.usecase.hospital.update_hospital import UpdateHospitalUseCase


class UpdateHospitalHandler:
    def __init__(self, update_hospital_usecase: UpdateHospitalUseCase):
        self.update_hospital_usecase = update_hospital_usecase

    def handle(self, hospital_id: uuid.UUID, hospital_data: UpdateHospitalDTO):
        try:
            hospital = self.update_hospital_usecase.execute(hospital_id, hospital_data)
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
            raise HTTPException(status_code=500, detail="Internal server error while updating hospital")
