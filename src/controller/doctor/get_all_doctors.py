from fastapi import HTTPException
from src.domain.usecase.doctor.get_all_doctors import GetAllDoctorsUseCase


class GetAllDoctorsHandler:
    def __init__(self, get_all_doctors_usecase: GetAllDoctorsUseCase):
        self.get_all_doctors_usecase = get_all_doctors_usecase

    def handle(self, skip: int = 0, limit: int = 100):
        try:
            doctors = self.get_all_doctors_usecase.execute(skip=skip, limit=limit)
            return [
                {
                    "id": str(doctor.id),
                    "name": doctor.name,
                    "crm": doctor.crm,
                    "specialty": doctor.specialty,
                    "phone": doctor.phone,
                    "email": doctor.email,
                    "created_at": doctor.created_at,
                    "updated_at": doctor.updated_at
                }
                for doctor in doctors
            ]
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error while fetching doctors")
