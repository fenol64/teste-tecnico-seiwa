from fastapi import APIRouter, Depends, status
from typing import List, Dict, Any
import uuid

from src.bootstrap.provider import usecase_factory
from src.infrastructure.auth.dependencies import get_current_user
from src.controller.doctor_hospital.assign_doctor_to_hospital import AssignDoctorToHospitalHandler
from src.controller.doctor_hospital.remove_doctor_from_hospital import RemoveDoctorFromHospitalHandler
from src.controller.doctor_hospital.get_hospitals_by_doctor import GetHospitalsByDoctorHandler
from src.controller.doctor_hospital.get_doctors_by_hospital import GetDoctorsByHospitalHandler
from src.domain.usecase.doctor_hospital.assign_doctor_to_hospital import AssignDoctorToHospitalUseCase
from src.domain.usecase.doctor_hospital.remove_doctor_from_hospital import RemoveDoctorFromHospitalUseCase
from src.domain.usecase.doctor_hospital.get_hospitals_by_doctor import GetHospitalsByDoctorUseCase
from src.domain.usecase.doctor_hospital.get_doctors_by_hospital import GetDoctorsByHospitalUseCase
from src.dto.doctorHospitalDTO import AssignDoctorToHospitalDTO, DoctorHospitalResponseDTO

router = APIRouter()

@router.post(
    '/assign',
    summary="Assign Doctor to Hospital",
    description="Creates a link between doctor and hospital",
    response_model=DoctorHospitalResponseDTO,
    status_code=status.HTTP_201_CREATED
)
async def assign_doctor_to_hospital(
    data: AssignDoctorToHospitalDTO,
    usecase: AssignDoctorToHospitalUseCase = Depends(usecase_factory('assign_doctor_to_hospital_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = AssignDoctorToHospitalHandler(assign_doctor_to_hospital_usecase=usecase)
    return handler.handle(uuid.UUID(data.doctor_id), uuid.UUID(data.hospital_id))


@router.delete(
    '/remove/{doctor_id}/{hospital_id}',
    summary="Remove Doctor from Hospital",
    description="Removes the link between doctor and hospital",
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
    '/doctor/{doctor_id}/hospitals',
    summary="List Hospitals by Doctor",
    description="Returns all hospitals where a doctor works",
    status_code=status.HTTP_200_OK
)
async def get_hospitals_by_doctor(
    doctor_id: uuid.UUID,
    usecase: GetHospitalsByDoctorUseCase = Depends(usecase_factory('get_hospitals_by_doctor_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = GetHospitalsByDoctorHandler(get_hospitals_by_doctor_usecase=usecase)
    return handler.handle(doctor_id)


@router.get(
    '/hospital/{hospital_id}/doctors',
    summary="List Doctors by Hospital",
    description="Returns all doctors working in a hospital",
    status_code=status.HTTP_200_OK
)
async def get_doctors_by_hospital(
    hospital_id: uuid.UUID,
    usecase: GetDoctorsByHospitalUseCase = Depends(usecase_factory('get_doctors_by_hospital_usecase')),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    handler = GetDoctorsByHospitalHandler(get_doctors_by_hospital_usecase=usecase)
    return handler.handle(hospital_id)
