from fastapi import APIRouter, Depends, status, Query
from typing import List
from uuid import UUID

from src.dto.pagination import PaginatedResponse
from src.bootstrap.provider import usecase_factory
from src.infrastructure.auth.dependencies import get_current_user
from src.controller.repasse.create_repasse import create_repasse_controller
from src.controller.repasse.get_all_repasses import get_all_repasses_controller
from src.controller.repasse.get_repasse_by_id import get_repasse_by_id_controller
from src.controller.repasse.get_repasses_by_production import get_repasses_by_production_controller
from src.controller.repasse.get_repasses_by_hospital import get_repasses_by_hospital_controller
from src.controller.repasse.update_repasse import update_repasse_controller
from src.controller.repasse.delete_repasse import delete_repasse_controller
from src.controller.repasse.get_repasse_stats import get_repasse_stats
from src.domain.usecase.repasse.create_repasse import CreateRepasseUseCase
from src.domain.usecase.repasse.get_all_repasses import GetAllRepassesUseCase
from src.domain.usecase.repasse.get_repasse_by_id import GetRepasseByIdUseCase
from src.domain.usecase.repasse.get_repasses_by_production import GetRepassesByProductionUseCase
from src.domain.usecase.repasse.get_repasses_by_hospital import GetRepassesByHospitalUseCase
from src.domain.usecase.repasse.update_repasse import UpdateRepasseUseCase
from src.domain.usecase.repasse.delete_repasse import DeleteRepasseUseCase
from src.dto.repasseDTO import CreateRepasseDTO, UpdateRepasseDTO, RepasseResponseDTO, RepasseStatsDTO
from src.dto.responses import DeleteResponseDTO

router = APIRouter()


@router.post(
    "/",
    summary="Create Repasse",
    description="Registers a new medical repasse linked to a production",
    response_model=RepasseResponseDTO,
    status_code=status.HTTP_201_CREATED
)
async def create_repasse(
    data: CreateRepasseDTO,
    usecase: CreateRepasseUseCase = Depends(usecase_factory('create_repasse_usecase')),
    current_user=Depends(get_current_user)
):
    user_id = UUID(current_user.get("sub"))
    return create_repasse_controller(data, user_id, usecase)


@router.get(
    "/",
    summary="List Repasses",
    description="Returns all registered repasses with pagination",
    response_model=PaginatedResponse[RepasseResponseDTO]
)
async def get_all_repasses(
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    usecase: GetAllRepassesUseCase = Depends(usecase_factory('get_all_repasses_usecase')),
    current_user=Depends(get_current_user)
):
    skip = (page - 1) * page_size
    user_id = UUID(current_user.get("sub"))
    return get_all_repasses_controller(usecase, user_id=user_id, skip=skip, limit=page_size)


@router.get(
    "/{repasse_id}",
    summary="Get Repasse by ID",
    description="Returns a specific repasse by ID",
    response_model=RepasseResponseDTO
)
async def get_repasse_by_id(
    repasse_id: UUID,
    usecase: GetRepasseByIdUseCase = Depends(usecase_factory('get_repasse_by_id_usecase')),
    current_user=Depends(get_current_user)
):
    return get_repasse_by_id_controller(repasse_id, usecase)


@router.get(
    "/production/{production_id}",
    summary="List Repasses by Production",
    description="Returns all repasses linked to a specific production",
    response_model=List[RepasseResponseDTO]
)
async def get_repasses_by_production(
    production_id: UUID,
    usecase: GetRepassesByProductionUseCase = Depends(usecase_factory('get_repasses_by_production_usecase')),
    current_user=Depends(get_current_user)
):
    return get_repasses_by_production_controller(production_id, usecase)


@router.get(
    "/hospital/{hospital_id}",
    summary="List Repasses by Hospital",
    description="Returns all repasses linked to a specific hospital",
    response_model=List[RepasseResponseDTO]
)
async def get_repasses_by_hospital(
    hospital_id: UUID,
    usecase: GetRepassesByHospitalUseCase = Depends(usecase_factory('get_repasses_by_hospital_usecase')),
    current_user=Depends(get_current_user)
):
    return get_repasses_by_hospital_controller(hospital_id, usecase)


@router.put(
    "/{repasse_id}",
    summary="Update Repasse",
    description="Updates the value of an existing repasse",
    response_model=RepasseResponseDTO
)
async def update_repasse(
    repasse_id: UUID,
    data: UpdateRepasseDTO,
    usecase: UpdateRepasseUseCase = Depends(usecase_factory('update_repasse_usecase')),
    current_user=Depends(get_current_user)
):
    return update_repasse_controller(repasse_id, data, usecase)


@router.delete(
    "/{repasse_id}",
    summary="Delete Repasse",
    description="Removes a repasse from the system",
    response_model=DeleteResponseDTO
)
async def delete_repasse(
    repasse_id: UUID,
    usecase: DeleteRepasseUseCase = Depends(usecase_factory('delete_repasse_usecase')),
    current_user=Depends(get_current_user)
):
    return delete_repasse_controller(repasse_id, usecase)


router.add_api_route(
    "/stats/{doctor_id}",
    get_repasse_stats,
    methods=["GET"],
    response_model=RepasseStatsDTO,
    summary="Doctor Repasse Statistics",
    description="Returns repasse statistics (pending vs consolidated) for a doctor in a date range"
)
