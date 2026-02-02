from uuid import UUID
from src.dto.repasseDTO import RepasseResponseDTO
from src.dto.pagination import PaginatedResponse
from src.domain.usecase.repasse.get_all_repasses import GetAllRepassesUseCase


def get_all_repasses_controller(
    usecase: GetAllRepassesUseCase,
    user_id: UUID,
    skip: int = 0,
    limit: int = 100
) -> PaginatedResponse[RepasseResponseDTO]:
    repasses, total = usecase.execute(skip=skip, limit=limit, user_id=user_id)
    items = [RepasseResponseDTO.model_validate(repasse) for repasse in repasses]

    page = (skip // limit) + 1 if limit > 0 else 1

    return PaginatedResponse.create(
        items=items,
        total=total,
        page=page,
        page_size=limit
    )
