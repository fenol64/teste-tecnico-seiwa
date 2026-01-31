from uuid import UUID
from src.dto.repasseDTO import UpdateRepasseDTO, RepasseResponseDTO
from src.domain.usecase.repasse.update_repasse import UpdateRepasseUseCase


def update_repasse_controller(repasse_id: UUID, data: UpdateRepasseDTO, usecase: UpdateRepasseUseCase) -> RepasseResponseDTO:
    repasse = usecase.execute(repasse_id, data)
    return RepasseResponseDTO.model_validate(repasse)
