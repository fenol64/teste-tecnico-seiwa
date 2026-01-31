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
from src.controller.doctor_hospital.assign_doctor_to_hospital import AssignDoctorToHospitalHandler
from src.controller.doctor_hospital.remove_doctor_from_hospital import RemoveDoctorFromHospitalHandler
from src.controller.doctor_hospital.get_hospitals_by_doctor import GetHospitalsByDoctorHandler
from src.domain.usecase.doctor.create_doctor import CreateDoctorUseCase
from src.domain.usecase.doctor.get_all_doctors import GetAllDoctorsUseCase
from src.domain.usecase.doctor.get_doctor_by_id import GetDoctorByIdUseCase
from src.domain.usecase.doctor.update_doctor import UpdateDoctorUseCase
from src.domain.usecase.doctor.delete_doctor import DeleteDoctorUseCase
from src.domain.usecase.doctor_hospital.assign_doctor_to_hospital import AssignDoctorToHospitalUseCase
from src.domain.usecase.doctor_hospital.remove_doctor_from_hospital import RemoveDoctorFromHospitalUseCase
from src.domain.usecase.doctor_hospital.get_hospitals_by_doctor import GetHospitalsByDoctorUseCase
from src.dto.doctorDTO import CreateDoctorDTO, UpdateDoctorDTO, DoctorResponseDTO
from src.dto.doctorHospitalDTO import DoctorHospitalResponseDTO

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


@router.post(
    '/{doctor_id}/hospitals/{hospital_id}',
    summary="Vincular Médico a Hospital",
    description="Cria um vínculo entre médico e hospital",
    response_model=DoctorHospitalResponseDTO,
    status_code=status.HTTP_201_CREATED
)
async def assign_doctor_to_hospital(
    doctor_id: uuid.UUID,
    hospital_id: uuid.UUID,
    usecase: AssignDoctorToHospitalUseCase = Depends(usecase_factory('assign_doctor_to_hospital_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = AssignDoctorToHospitalHandler(assign_doctor_to_hospital_usecase=usecase)
    return handler.handle(doctor_id, hospital_id)


@router.delete(
    '/{doctor_id}/hospitals/{hospital_id}',
    summary="Remover Médico de Hospital",
    description="Remove o vínculo entre médico e hospital",
    status_code=status.HTTP_200_OK
)
async def remove_doctor_from_hospital(
    doctor_id: uuid.UUID,
    hospital_id: uuid.UUID,
    usecase: RemoveDoctorFromHospitalUseCase = Depends(usecase_factory('remove_doctor_from_hospital_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = RemoveDoctorFromHospitalHandler(remove_doctor_from_hospital_usecase=usecase)
    return handler.handle(doctor_id, hospital_id)


@router.get(
    '/{doctor_id}/hospitals',
    summary="Listar Hospitais de um Médico",
    description="Retorna todos os hospitais onde um médico atua",
    status_code=status.HTTP_200_OK
)
async def get_hospitals_by_doctor(
    doctor_id: uuid.UUID,
    usecase: GetHospitalsByDoctorUseCase = Depends(usecase_factory('get_hospitals_by_doctor_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = GetHospitalsByDoctorHandler(get_hospitals_by_doctor_usecase=usecase)
    return handler.handle(doctor_id)
