from fastapi import APIRouter, Depends, status, Query
from typing import List, Dict, Any
import uuid

from src.bootstrap.provider import usecase_factory
from src.infrastructure.auth.dependencies import get_current_user
from src.controller.hospital.create_hospital import CreateHospitalHandler
from src.controller.hospital.get_all_hospitals import GetAllHospitalsHandler
from src.controller.hospital.get_hospital_by_id import GetHospitalByIdHandler
from src.controller.hospital.update_hospital import UpdateHospitalHandler
from src.controller.hospital.delete_hospital import DeleteHospitalHandler
from src.controller.doctor_hospital.get_doctors_by_hospital import GetDoctorsByHospitalHandler
from src.domain.usecase.hospital.create_hospital import CreateHospitalUseCase
from src.domain.usecase.hospital.get_all_hospitals import GetAllHospitalsUseCase
from src.domain.usecase.hospital.get_hospital_by_id import GetHospitalByIdUseCase
from src.domain.usecase.hospital.update_hospital import UpdateHospitalUseCase
from src.domain.usecase.hospital.delete_hospital import DeleteHospitalUseCase
from src.domain.usecase.doctor_hospital.get_doctors_by_hospital import GetDoctorsByHospitalUseCase
from src.dto.hospitalDTO import CreateHospitalDTO, UpdateHospitalDTO, HospitalResponseDTO

router = APIRouter()

@router.post(
    '/',
    summary="Criar Hospital",
    description="Cria um novo hospital no sistema",
    response_model=HospitalResponseDTO,
    status_code=status.HTTP_201_CREATED
)
async def create_hospital(
    hospital: CreateHospitalDTO,
    usecase: CreateHospitalUseCase = Depends(usecase_factory('create_hospital_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = CreateHospitalHandler(create_hospital_usecase=usecase)
    return handler.handle(hospital)


@router.get(
    '/',
    summary="Listar Hospitais",
    description="Lista todos os hospitais cadastrados com paginação",
    response_model=List[HospitalResponseDTO],
    status_code=status.HTTP_200_OK
)
async def get_all_hospitals(
    skip: int = Query(0, ge=0, description="Número de registros a pular"),
    limit: int = Query(100, ge=1, le=100, description="Número máximo de registros a retornar"),
    usecase: GetAllHospitalsUseCase = Depends(usecase_factory('get_all_hospitals_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = GetAllHospitalsHandler(get_all_hospitals_usecase=usecase)
    return handler.handle(skip=skip, limit=limit)


@router.get(
    '/{hospital_id}',
    summary="Obter Hospital por ID",
    description="Retorna os dados de um hospital específico",
    response_model=HospitalResponseDTO,
    status_code=status.HTTP_200_OK
)
async def get_hospital_by_id(
    hospital_id: uuid.UUID,
    usecase: GetHospitalByIdUseCase = Depends(usecase_factory('get_hospital_by_id_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = GetHospitalByIdHandler(get_hospital_by_id_usecase=usecase)
    return handler.handle(hospital_id)


@router.put(
    '/{hospital_id}',
    summary="Atualizar Hospital",
    description="Atualiza os dados de um hospital existente",
    response_model=HospitalResponseDTO,
    status_code=status.HTTP_200_OK
)
async def update_hospital(
    hospital_id: uuid.UUID,
    hospital: UpdateHospitalDTO,
    usecase: UpdateHospitalUseCase = Depends(usecase_factory('update_hospital_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = UpdateHospitalHandler(update_hospital_usecase=usecase)
    return handler.handle(hospital_id, hospital)


@router.delete(
    '/{hospital_id}',
    summary="Deletar Hospital",
    description="Remove um hospital do sistema",
    status_code=status.HTTP_200_OK
)
async def delete_hospital(
    hospital_id: uuid.UUID,
    usecase: DeleteHospitalUseCase = Depends(usecase_factory('delete_hospital_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = DeleteHospitalHandler(delete_hospital_usecase=usecase)
    return handler.handle(hospital_id)


@router.get(
    '/{hospital_id}/doctors',
    summary="Listar Médicos de um Hospital",
    description="Retorna todos os médicos que atuam em um hospital",
    status_code=status.HTTP_200_OK
)
async def get_doctors_by_hospital(
    hospital_id: uuid.UUID,
    usecase: GetDoctorsByHospitalUseCase = Depends(usecase_factory('get_doctors_by_hospital_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = GetDoctorsByHospitalHandler(get_doctors_by_hospital_usecase=usecase)
    return handler.handle(hospital_id)
