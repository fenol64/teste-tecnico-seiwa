from uuid import UUID
from src.dto.responses import DeleteResponseDTO
from src.domain.usecase.repasse.delete_repasse import DeleteRepasseUseCase


def delete_repasse_controller(repasse_id: UUID, usecase: DeleteRepasseUseCase) -> DeleteResponseDTO:
    usecase.execute(repasse_id)
    return DeleteResponseDTO(message="Repasse deleted successfully")
