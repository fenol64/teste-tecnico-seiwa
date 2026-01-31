from src.domain.usecase.interfaces.IGetProductionById import IGetProductionById
from typing import Optional
import uuid
from src.domain.entities.Production import Production


class GetProductionByIdUseCase:
    def __init__(self, get_production_by_id_port: IGetProductionById):
        self.get_production_by_id_port = get_production_by_id_port

    def execute(self, production_id: uuid.UUID) -> Optional[Production]:
        production = self.get_production_by_id_port.get_by_id(production_id)
        if not production:
            raise ValueError("Production not found.")
        return production
