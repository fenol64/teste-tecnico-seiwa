from fastapi import HTTPException
from src.domain.usecase.production.get_all_productions import GetAllProductionsUseCase
from src.dto.pagination import PaginatedResponse
from src.dto.productionDTO import ProductionResponseDTO


import uuid

class GetAllProductionsHandler:
    def __init__(self, get_all_productions_usecase: GetAllProductionsUseCase):
        self.get_all_productions_usecase = get_all_productions_usecase

    def handle(self, user_id: str, skip: int = 0, limit: int = 100) -> PaginatedResponse[ProductionResponseDTO]:
        try:
            productions, total = self.get_all_productions_usecase.execute(skip=skip, limit=limit, user_id=uuid.UUID(user_id))
            items = [
                ProductionResponseDTO(
                    id=str(production.id),
                    doctor_id=str(production.doctor_id),
                    hospital_id=str(production.hospital_id),
                    type=production.type,
                    date=production.date.isoformat(),
                    description=production.description,
                    created_at=production.created_at,
                    updated_at=production.updated_at
                )
                for production in productions
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
            raise HTTPException(status_code=500, detail="Internal server error while fetching productions")
