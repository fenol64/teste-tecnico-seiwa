from fastapi import HTTPException
import uuid
from src.domain.usecase.production.get_production_by_id import GetProductionByIdUseCase


class GetProductionByIdHandler:
    def __init__(self, get_production_by_id_usecase: GetProductionByIdUseCase):
        self.get_production_by_id_usecase = get_production_by_id_usecase

    def handle(self, production_id: uuid.UUID):
        try:
            production = self.get_production_by_id_usecase.execute(production_id)
            return {
                "id": str(production.id),
                "doctor_id": str(production.doctor_id),
                "hospital_id": str(production.hospital_id),
                "type": production.type,
                "date": production.date.isoformat() if hasattr(production.date, 'isoformat') else str(production.date),
                "description": production.description,
                "created_at": production.created_at,
                "updated_at": production.updated_at
            }
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error while fetching production")
