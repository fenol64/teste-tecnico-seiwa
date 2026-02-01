from fastapi import HTTPException
from src.domain.usecase.doctor.get_all_doctors import GetAllDoctorsUseCase
from src.dto.pagination import PaginatedResponse
from src.dto.doctorDTO import DoctorResponseDTO


class GetAllDoctorsHandler:
    def __init__(self, get_all_doctors_usecase: GetAllDoctorsUseCase):
        self.get_all_doctors_usecase = get_all_doctors_usecase

    def handle(self, skip: int = 0, limit: int = 100) -> PaginatedResponse[DoctorResponseDTO]:
        try:
            doctors, total = self.get_all_doctors_usecase.execute(skip=skip, limit=limit)
            items = [
                DoctorResponseDTO(
                    id=str(doctor.id),
                    name=doctor.name,
                    crm=doctor.crm,
                    specialty=doctor.specialty,
                    phone=doctor.phone,
                    email=doctor.email,
                    created_at=doctor.created_at,
                    updated_at=doctor.updated_at
                )
                for doctor in doctors
            ]

            page = (skip // limit) + 1 if limit > 0 else 1
            return PaginatedResponse.create(
                items=items,
                total=total,
                page=page,
                page_size=limit
            )
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error while fetching doctors")
