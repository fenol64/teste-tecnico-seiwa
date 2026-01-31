from typing import List
from src.dto.repasseDTO import RepasseResponseDTO
from src.domain.usecase.repasse.get_all_repasses import GetAllRepassesUseCase


def get_all_repasses_controller(usecase: GetAllRepassesUseCase) -> List[RepasseResponseDTO]:
    repasses = usecase.execute()
    return [RepasseResponseDTO.model_validate(repasse) for repasse in repasses]
