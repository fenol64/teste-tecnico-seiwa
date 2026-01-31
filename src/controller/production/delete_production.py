from fastapi import HTTPException
import uuid
from src.domain.usecase.production.delete_production import DeleteProductionUseCase


class DeleteProductionHandler:
    def __init__(self, delete_production_usecase: DeleteProductionUseCase):
        self.delete_production_usecase = delete_production_usecase

    def handle(self, production_id: uuid.UUID):
        try:
            self.delete_production_usecase.execute(production_id)
            return {"message": "Production deleted successfully"}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error while deleting production")
