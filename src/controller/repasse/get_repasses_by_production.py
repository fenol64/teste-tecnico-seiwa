from typing import List
from uuid import UUID
from src.dto.repasseDTO import RepasseResponseDTO
from src.domain.usecase.repasse.get_repasses_by_production import GetRepassesByProductionUseCase


def get_repasses_by_production_controller(production_id: UUID, usecase: GetRepassesByProductionUseCase) -> List[RepasseResponseDTO]:
    repasses = usecase.execute(production_id)
    return [RepasseResponseDTO.model_validate(repasse) for repasse in repasses]
