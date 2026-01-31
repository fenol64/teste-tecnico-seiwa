from src.domain.usecase.interfaces.IUpdateProduction import IUpdateProduction
from src.domain.usecase.interfaces.IGetProductionById import IGetProductionById
from src.dto.productionDTO import UpdateProductionDTO
from typing import Optional
import uuid
from src.domain.entities.Production import Production


class UpdateProductionUseCase:
    def __init__(
        self,
        update_production_port: IUpdateProduction,
        get_production_by_id_port: IGetProductionById
    ):
        self.update_production_port = update_production_port
        self.get_production_by_id_port = get_production_by_id_port

    def execute(self, production_id: uuid.UUID, production_data: UpdateProductionDTO) -> Optional[Production]:
        # Verifica se a produção existe
        existing_production = self.get_production_by_id_port.get_by_id(production_id)
        if not existing_production:
            raise ValueError("Production not found.")

        # Prepara dados para atualização (apenas campos não nulos)
        update_data = {}
        if production_data.type is not None:
            update_data['type'] = production_data.type.value
        if production_data.date is not None:
            update_data['date'] = production_data.date
        if production_data.description is not None:
            update_data['description'] = production_data.description

        if not update_data:
            return existing_production

        updated_production = self.update_production_port.update(production_id, **update_data)
        return updated_production
