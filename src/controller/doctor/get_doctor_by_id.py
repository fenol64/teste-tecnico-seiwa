from fastapi import HTTPException
import uuid
from src.domain.usecase.doctor.get_doctor_by_id import GetDoctorByIdUseCase


class GetDoctorByIdHandler:
    def __init__(self, get_doctor_by_id_usecase: GetDoctorByIdUseCase):
        self.get_doctor_by_id_usecase = get_doctor_by_id_usecase

    def handle(self, doctor_id: uuid.UUID):
        try:
            doctor = self.get_doctor_by_id_usecase.execute(doctor_id)
            return {
                "id": str(doctor.id),
                "name": doctor.name,
                "crm": doctor.crm,
                "specialty": doctor.specialty,
                "phone": doctor.phone,
                "email": doctor.email,
                "created_at": doctor.created_at,
                "updated_at": doctor.updated_at
            }
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error while fetching doctor")
