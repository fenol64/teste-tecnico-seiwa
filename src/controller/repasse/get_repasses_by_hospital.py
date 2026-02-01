from typing import List
from uuid import UUID
from src.dto.repasseDTO import RepasseResponseDTO
from src.domain.usecase.repasse.get_repasses_by_hospital import GetRepassesByHospitalUseCase

def get_repasses_by_hospital_controller(hospital_id: UUID, usecase: GetRepassesByHospitalUseCase) -> List[RepasseResponseDTO]:
    repasses = usecase.execute(hospital_id)
    return [RepasseResponseDTO.model_validate(repasse) for repasse in repasses]
