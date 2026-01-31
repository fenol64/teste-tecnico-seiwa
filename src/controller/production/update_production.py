from fastapi import HTTPException
import uuid
from src.dto.productionDTO import UpdateProductionDTO
from src.domain.usecase.production.update_production import UpdateProductionUseCase


class UpdateProductionHandler:
    def __init__(self, update_production_usecase: UpdateProductionUseCase):
        self.update_production_usecase = update_production_usecase

    def handle(self, production_id: uuid.UUID, production_data: UpdateProductionDTO):
        try:
            production = self.update_production_usecase.execute(production_id, production_data)
            return {
                "id": str(production.id),
                "doctor_id": str(production.doctor_id),
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
            raise HTTPException(status_code=500, detail="Internal server error while updating production")
