from fastapi import HTTPException
from src.domain.usecase.production.get_all_productions import GetAllProductionsUseCase


class GetAllProductionsHandler:
    def __init__(self, get_all_productions_usecase: GetAllProductionsUseCase):
        self.get_all_productions_usecase = get_all_productions_usecase

    def handle(self, skip: int = 0, limit: int = 100):
        try:
            productions = self.get_all_productions_usecase.execute(skip=skip, limit=limit)
            return [
                {
                    "id": str(production.id),
                    "doctor_id": str(production.doctor_id),
                    "hospital_id": str(production.hospital_id),
                    "type": production.type,
                    "date": production.date.isoformat() if hasattr(production.date, 'isoformat') else str(production.date),
                    "description": production.description,
                    "created_at": production.created_at,
                    "updated_at": production.updated_at
                }
                for production in productions
            ]
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error while fetching productions")
