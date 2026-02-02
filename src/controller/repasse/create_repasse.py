from uuid import UUID
from src.dto.repasseDTO import CreateRepasseDTO, RepasseResponseDTO
from src.domain.usecase.repasse.create_repasse import CreateRepasseUseCase


def create_repasse_controller(data: CreateRepasseDTO, user_id: UUID, usecase: CreateRepasseUseCase) -> RepasseResponseDTO:
    repasse = usecase.execute(data, user_id)
    return RepasseResponseDTO.model_validate(repasse)
