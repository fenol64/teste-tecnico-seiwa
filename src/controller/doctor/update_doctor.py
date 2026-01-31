from fastapi import HTTPException
import uuid
from src.dto.doctorDTO import UpdateDoctorDTO
from src.domain.usecase.doctor.update_doctor import UpdateDoctorUseCase


class UpdateDoctorHandler:
    def __init__(self, update_doctor_usecase: UpdateDoctorUseCase):
        self.update_doctor_usecase = update_doctor_usecase

    def handle(self, doctor_id: uuid.UUID, doctor_data: UpdateDoctorDTO):
        try:
            doctor = self.update_doctor_usecase.execute(doctor_id, doctor_data)
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
            raise HTTPException(status_code=500, detail="Internal server error while updating doctor")
