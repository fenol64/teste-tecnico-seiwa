from fastapi import HTTPException
import uuid
from src.domain.usecase.doctor.delete_doctor import DeleteDoctorUseCase


class DeleteDoctorHandler:
    def __init__(self, delete_doctor_usecase: DeleteDoctorUseCase):
        self.delete_doctor_usecase = delete_doctor_usecase

    def handle(self, doctor_id: uuid.UUID):
        try:
            self.delete_doctor_usecase.execute(doctor_id)
            return {"message": "Doctor deleted successfully"}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error while deleting doctor")
