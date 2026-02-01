from fastapi import HTTPException
from src.domain.usecase.hospital.get_all_hospitals import GetAllHospitalsUseCase
from src.dto.pagination import PaginatedResponse
from src.dto.hospitalDTO import HospitalResponseDTO


class GetAllHospitalsHandler:
    def __init__(self, get_all_hospitals_usecase: GetAllHospitalsUseCase):
        self.get_all_hospitals_usecase = get_all_hospitals_usecase

    def handle(self, skip: int = 0, limit: int = 100) -> PaginatedResponse[HospitalResponseDTO]:
        try:
            hospitals, total = self.get_all_hospitals_usecase.execute(skip=skip, limit=limit)
            items = [
                HospitalResponseDTO(
                    id=str(hospital.id),
                    name=hospital.name,
                    address=hospital.address,
                    created_at=hospital.created_at,
                    updated_at=hospital.updated_at
                )
                for hospital in hospitals
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
            raise HTTPException(status_code=500, detail="Internal server error while fetching hospitals")
