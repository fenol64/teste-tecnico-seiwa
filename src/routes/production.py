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
    summary="Criar Produção",
    description="Registra uma nova produção médica (plantão ou consulta)",
    response_model=ProductionResponseDTO,
    status_code=status.HTTP_201_CREATED
)
async def create_production(
    production: CreateProductionDTO,
    usecase: CreateProductionUseCase = Depends(usecase_factory('create_production_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = CreateProductionHandler(create_production_usecase=usecase)
    return handler.handle(production)


@router.get(
    '/',
    summary="Listar Produções",
    description="Lista todas as produções registradas com paginação",
    response_model=PaginatedResponse[ProductionResponseDTO],
    status_code=status.HTTP_200_OK
)
async def get_all_productions(
    page: int = Query(1, ge=1, description="Número da página (começa em 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Quantidade de itens por página"),
    usecase: GetAllProductionsUseCase = Depends(usecase_factory('get_all_productions_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    skip = (page - 1) * page_size
    handler = GetAllProductionsHandler(get_all_productions_usecase=usecase)
    return handler.handle(skip=skip, limit=page_size)


@router.get(
    '/{production_id}',
    summary="Obter Produção por ID",
    description="Retorna os dados de uma produção específica",
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
    summary="Listar Produções por Médico",
    description="Lista todas as produções de um médico específico",
    response_model=List[ProductionResponseDTO],
    status_code=status.HTTP_200_OK
)
async def get_productions_by_doctor(
    doctor_id: uuid.UUID,
    skip: int = Query(0, ge=0, description="Número de registros a pular"),
    limit: int = Query(100, ge=1, le=100, description="Número máximo de registros a retornar"),
    usecase: GetProductionsByDoctorUseCase = Depends(usecase_factory('get_productions_by_doctor_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = GetProductionsByDoctorHandler(get_productions_by_doctor_usecase=usecase)
    return handler.handle(doctor_id, skip=skip, limit=limit)


@router.get(
    '/hospital/{hospital_id}',
    summary="Listar Produções por Hospital",
    description="Lista todas as produções de um hospital específico",
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
    summary="Atualizar Produção",
    description="Atualiza os dados de uma produção existente",
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
    summary="Deletar Produção",
    description="Remove uma produção do sistema",
    status_code=status.HTTP_200_OK
)
async def delete_production(
    production_id: uuid.UUID,
    usecase: DeleteProductionUseCase = Depends(usecase_factory('delete_production_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = DeleteProductionHandler(delete_production_usecase=usecase)
    return handler.handle(production_id)
