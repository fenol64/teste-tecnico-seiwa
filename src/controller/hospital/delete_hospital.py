from fastapi import HTTPException
import uuid
from src.domain.usecase.hospital.delete_hospital import DeleteHospitalUseCase


class DeleteHospitalHandler:
    def __init__(self, delete_hospital_usecase: DeleteHospitalUseCase):
        self.delete_hospital_usecase = delete_hospital_usecase

    def handle(self, hospital_id: uuid.UUID):
        try:
            self.delete_hospital_usecase.execute(hospital_id)
            return {"message": "Hospital deleted successfully"}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error while deleting hospital")
