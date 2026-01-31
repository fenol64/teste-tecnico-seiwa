from uuid import UUID
from src.dto.repasseDTO import RepasseResponseDTO
from src.domain.usecase.repasse.get_repasse_by_id import GetRepasseByIdUseCase


def get_repasse_by_id_controller(repasse_id: UUID, usecase: GetRepasseByIdUseCase) -> RepasseResponseDTO:
    repasse = usecase.execute(repasse_id)
    return RepasseResponseDTO.model_validate(repasse)
