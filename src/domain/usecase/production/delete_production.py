from src.domain.usecase.interfaces.IDeleteProduction import IDeleteProduction
from src.domain.usecase.interfaces.IGetProductionById import IGetProductionById
import uuid


class DeleteProductionUseCase:
    def __init__(
        self,
        delete_production_port: IDeleteProduction,
        get_production_by_id_port: IGetProductionById
    ):
        self.delete_production_port = delete_production_port
        self.get_production_by_id_port = get_production_by_id_port

    def execute(self, production_id: uuid.UUID) -> bool:
        # Verifica se a produção existe
        existing_production = self.get_production_by_id_port.get_by_id(production_id)
        if not existing_production:
            raise ValueError("Production not found.")

        return self.delete_production_port.delete(production_id)
