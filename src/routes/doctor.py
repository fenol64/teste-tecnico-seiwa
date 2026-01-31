from fastapi import APIRouter, Depends, status, Query
from typing import List, Dict, Any
import uuid

from src.bootstrap.provider import usecase_factory
from src.infrastructure.auth.dependencies import get_current_user
from src.controller.doctor.create_doctor import CreateDoctorHandler
from src.controller.doctor.get_all_doctors import GetAllDoctorsHandler
from src.controller.doctor.get_doctor_by_id import GetDoctorByIdHandler
from src.controller.doctor.update_doctor import UpdateDoctorHandler
from src.controller.doctor.delete_doctor import DeleteDoctorHandler
from src.domain.usecase.doctor.create_doctor import CreateDoctorUseCase
from src.domain.usecase.doctor.get_all_doctors import GetAllDoctorsUseCase
from src.domain.usecase.doctor.get_doctor_by_id import GetDoctorByIdUseCase
from src.domain.usecase.doctor.update_doctor import UpdateDoctorUseCase
from src.domain.usecase.doctor.delete_doctor import DeleteDoctorUseCase
from src.dto.doctorDTO import CreateDoctorDTO, UpdateDoctorDTO, DoctorResponseDTO

router = APIRouter()

@router.post(
    '/',
    summary="Criar Médico",
    description="Cria um novo médico no sistema",
    response_model=DoctorResponseDTO,
    status_code=status.HTTP_201_CREATED
)
async def create_doctor(
    doctor: CreateDoctorDTO,
    usecase: CreateDoctorUseCase = Depends(usecase_factory('create_doctor_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = CreateDoctorHandler(create_doctor_usecase=usecase)
    return handler.handle(doctor)


@router.get(
    '/',
    summary="Listar Médicos",
    description="Lista todos os médicos cadastrados com paginação",
    response_model=List[DoctorResponseDTO],
    status_code=status.HTTP_200_OK
)
async def get_all_doctors(
    skip: int = Query(0, ge=0, description="Número de registros a pular"),
    limit: int = Query(100, ge=1, le=100, description="Número máximo de registros a retornar"),
    usecase: GetAllDoctorsUseCase = Depends(usecase_factory('get_all_doctors_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = GetAllDoctorsHandler(get_all_doctors_usecase=usecase)
    return handler.handle(skip=skip, limit=limit)


@router.get(
    '/{doctor_id}',
    summary="Obter Médico por ID",
    description="Retorna os dados de um médico específico",
    response_model=DoctorResponseDTO,
    status_code=status.HTTP_200_OK
)
async def get_doctor_by_id(
    doctor_id: uuid.UUID,
    usecase: GetDoctorByIdUseCase = Depends(usecase_factory('get_doctor_by_id_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = GetDoctorByIdHandler(get_doctor_by_id_usecase=usecase)
    return handler.handle(doctor_id)


@router.put(
    '/{doctor_id}',
    summary="Atualizar Médico",
    description="Atualiza os dados de um médico existente",
    response_model=DoctorResponseDTO,
    status_code=status.HTTP_200_OK
)
async def update_doctor(
    doctor_id: uuid.UUID,
    doctor: UpdateDoctorDTO,
    usecase: UpdateDoctorUseCase = Depends(usecase_factory('update_doctor_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = UpdateDoctorHandler(update_doctor_usecase=usecase)
    return handler.handle(doctor_id, doctor)


@router.delete(
    '/{doctor_id}',
    summary="Deletar Médico",
    description="Remove um médico do sistema",
    status_code=status.HTTP_200_OK
)
async def delete_doctor(
    doctor_id: uuid.UUID,
    usecase: DeleteDoctorUseCase = Depends(usecase_factory('delete_doctor_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = DeleteDoctorHandler(delete_doctor_usecase=usecase)
    return handler.handle(doctor_id)
