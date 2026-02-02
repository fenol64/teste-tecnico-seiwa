from fastapi import APIRouter, Depends, status, Query
from typing import List, Dict, Any
import uuid

from src.dto.pagination import PaginatedResponse
from src.bootstrap.provider import usecase_factory
from src.infrastructure.auth.dependencies import get_current_user
from src.controller.production.create_production import CreateProductionHandler
from src.controller.production.get_all_productions import GetAllProductionsHandler
from src.controller.production.get_production_by_id import GetProductionByIdHandler
from src.controller.production.get_productions_by_doctor import GetProductionsByDoctorHandler
from src.controller.production.get_productions_by_hospital import GetProductionsByHospitalHandler
from src.controller.production.update_production import UpdateProductionHandler
from src.controller.production.delete_production import DeleteProductionHandler
from src.domain.usecase.production.create_production import CreateProductionUseCase
from src.domain.usecase.production.get_all_productions import GetAllProductionsUseCase
from src.domain.usecase.production.get_production_by_id import GetProductionByIdUseCase
from src.domain.usecase.production.get_productions_by_doctor import GetProductionsByDoctorUseCase
from src.domain.usecase.production.get_productions_by_hospital import GetProductionsByHospitalUseCase
from src.domain.usecase.production.update_production import UpdateProductionUseCase
from src.domain.usecase.production.delete_production import DeleteProductionUseCase
from src.dto.productionDTO import CreateProductionDTO, UpdateProductionDTO, ProductionResponseDTO

router = APIRouter()

@router.post(
    '/',
    summary="Create Production",
    description="Registers a new medical production (shift or consultation)",
    response_model=ProductionResponseDTO,
    status_code=status.HTTP_201_CREATED
)
async def create_production(
    production: CreateProductionDTO,
    usecase: CreateProductionUseCase = Depends(usecase_factory('create_production_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = CreateProductionHandler(create_production_usecase=usecase)
    user_id = current_user.get("sub")
    return handler.handle(production, user_id)


@router.get(
    '/',
    summary="List Productions",
    description="Lists all registered productions with pagination",
    response_model=PaginatedResponse[ProductionResponseDTO],
    status_code=status.HTTP_200_OK
)
async def get_all_productions(
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    usecase: GetAllProductionsUseCase = Depends(usecase_factory('get_all_productions_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    skip = (page - 1) * page_size
    handler = GetAllProductionsHandler(get_all_productions_usecase=usecase)
    user_id = current_user.get("sub")
    return handler.handle(user_id=user_id, skip=skip, limit=page_size)


@router.get(
    '/{production_id}',
    summary="Get Production by ID",
    description="Returns data for a specific production",
    response_model=ProductionResponseDTO,
    status_code=status.HTTP_200_OK
)
async def get_production_by_id(
    production_id: uuid.UUID,
    usecase: GetProductionByIdUseCase = Depends(usecase_factory('get_production_by_id_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = GetProductionByIdHandler(get_production_by_id_usecase=usecase)
    return handler.handle(production_id)


@router.get(
    '/doctor/{doctor_id}',
    summary="List Productions by Doctor",
    description="Lists all productions for a specific doctor",
    response_model=List[ProductionResponseDTO],
    status_code=status.HTTP_200_OK
)
async def get_productions_by_doctor(
    doctor_id: uuid.UUID,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    usecase: GetProductionsByDoctorUseCase = Depends(usecase_factory('get_productions_by_doctor_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = GetProductionsByDoctorHandler(get_productions_by_doctor_usecase=usecase)
    return handler.handle(doctor_id, skip=skip, limit=limit)


@router.get(
    '/hospital/{hospital_id}',
    summary="List Productions by Hospital",
    description="Lists all productions for a specific hospital",
    response_model=List[ProductionResponseDTO],
    status_code=status.HTTP_200_OK
)
async def get_productions_by_hospital(
    hospital_id: uuid.UUID,
    usecase: GetProductionsByHospitalUseCase = Depends(usecase_factory('get_productions_by_hospital_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = GetProductionsByHospitalHandler(usecase=usecase)
    return handler.handle(hospital_id)


@router.put(
    '/{production_id}',
    summary="Update Production",
    description="Updates data of an existing production",
    response_model=ProductionResponseDTO,
    status_code=status.HTTP_200_OK
)
async def update_production(
    production_id: uuid.UUID,
    production: UpdateProductionDTO,
    usecase: UpdateProductionUseCase = Depends(usecase_factory('update_production_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = UpdateProductionHandler(update_production_usecase=usecase)
    return handler.handle(production_id, production)


@router.delete(
    '/{production_id}',
    summary="Delete Production",
    description="Removes a production from the system",
    status_code=status.HTTP_200_OK
)
async def delete_production(
    production_id: uuid.UUID,
    usecase: DeleteProductionUseCase = Depends(usecase_factory('delete_production_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = DeleteProductionHandler(delete_production_usecase=usecase)
    return handler.handle(production_id)
