from fastapi import HTTPException
import uuid
from src.domain.usecase.production.get_productions_by_hospital import GetProductionsByHospitalUseCase

class GetProductionsByHospitalHandler:
    def __init__(self, usecase: GetProductionsByHospitalUseCase):
        self.usecase = usecase

    def handle(self, hospital_id: uuid.UUID):
        try:
            productions = self.usecase.execute(hospital_id)
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
            raise HTTPException(status_code=500, detail=str(e))
