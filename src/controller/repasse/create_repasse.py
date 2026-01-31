from src.dto.repasseDTO import CreateRepasseDTO, RepasseResponseDTO
from src.domain.usecase.repasse.create_repasse import CreateRepasseUseCase


def create_repasse_controller(data: CreateRepasseDTO, usecase: CreateRepasseUseCase) -> RepasseResponseDTO:
    repasse = usecase.execute(data)
    return RepasseResponseDTO.model_validate(repasse)
