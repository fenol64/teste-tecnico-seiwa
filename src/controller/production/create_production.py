from fastapi import HTTPException
from src.dto.productionDTO import CreateProductionDTO
from src.domain.usecase.production.create_production import CreateProductionUseCase


class CreateProductionHandler:
    def __init__(self, create_production_usecase: CreateProductionUseCase):
        self.create_production_usecase = create_production_usecase

    def handle(self, production_data: CreateProductionDTO):
        try:
            production = self.create_production_usecase.execute(production_data)
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
            raise HTTPException(status_code=500, detail="Internal server error while creating production")
