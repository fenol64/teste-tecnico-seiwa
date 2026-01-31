from fastapi import HTTPException
from src.dto.doctorDTO import CreateDoctorDTO
from src.domain.usecase.doctor.create_doctor import CreateDoctorUseCase


class CreateDoctorHandler:
    def __init__(self, create_doctor_usecase: CreateDoctorUseCase):
        self.create_doctor_usecase = create_doctor_usecase

    def handle(self, doctor_data: CreateDoctorDTO):
        try:
            doctor = self.create_doctor_usecase.execute(doctor_data)
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
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error while creating doctor")
