from sqlalchemy.orm import Session
from typing import List
import uuid

from src.infrastructure.database.models.doctor_hospital_model import DoctorHospitalModel
from src.domain.usecase.interfaces.IAssignDoctorToHospital import IAssignDoctorToHospital
from src.domain.usecase.interfaces.IRemoveDoctorFromHospital import IRemoveDoctorFromHospital
from src.domain.usecase.interfaces.IGetHospitalsByDoctor import IGetHospitalsByDoctor
from src.domain.usecase.interfaces.IGetDoctorsByHospital import IGetDoctorsByHospital


class DoctorHospitalRepository(IAssignDoctorToHospital, IRemoveDoctorFromHospital, IGetHospitalsByDoctor, IGetDoctorsByHospital):
    def __init__(self, db: Session):
        self.db = db

    def assign_doctor_to_hospital(self, doctor_id: uuid.UUID, hospital_id: uuid.UUID) -> dict:
        """Vincula um médico a um hospital"""
        # Verifica se o vínculo já existe
        existing = self.db.query(DoctorHospitalModel).filter(
            DoctorHospitalModel.doctor_id == doctor_id,
            DoctorHospitalModel.hospital_id == hospital_id
        ).first()

        if existing:
            return {
                "doctor_id": str(existing.doctor_id),
                "hospital_id": str(existing.hospital_id),
                "created_at": existing.created_at.isoformat()
            }

        # Cria novo vínculo
        doctor_hospital = DoctorHospitalModel(
            doctor_id=doctor_id,
            hospital_id=hospital_id
        )

        self.db.add(doctor_hospital)
        self.db.commit()
        self.db.refresh(doctor_hospital)

        return {
            "doctor_id": str(doctor_hospital.doctor_id),
            "hospital_id": str(doctor_hospital.hospital_id),
            "created_at": doctor_hospital.created_at.isoformat()
        }

    def remove_doctor_from_hospital(self, doctor_id: uuid.UUID, hospital_id: uuid.UUID) -> bool:
        """Remove o vínculo entre médico e hospital"""
        doctor_hospital = self.db.query(DoctorHospitalModel).filter(
            DoctorHospitalModel.doctor_id == doctor_id,
            DoctorHospitalModel.hospital_id == hospital_id
        ).first()

        if not doctor_hospital:
            return False

        self.db.delete(doctor_hospital)
        self.db.commit()
        return True

    def get_hospitals_by_doctor(self, doctor_id: uuid.UUID) -> List[dict]:
        """Lista todos os hospitais de um médico"""
        from src.infrastructure.database.models.hospital_model import HospitalModel

        results = self.db.query(HospitalModel, DoctorHospitalModel).join(
            DoctorHospitalModel,
            HospitalModel.id == DoctorHospitalModel.hospital_id
        ).filter(
            DoctorHospitalModel.doctor_id == doctor_id
        ).all()

        return [
            {
                "id": str(hospital.id),
                "name": hospital.name,
                "address": hospital.address,
                "assigned_at": dh.created_at.isoformat()
            }
            for hospital, dh in results
        ]

    def get_doctors_by_hospital(self, hospital_id: uuid.UUID) -> List[dict]:
        """Lista todos os médicos de um hospital"""
        from src.infrastructure.database.models.doctor_model import DoctorModel

        results = self.db.query(DoctorModel, DoctorHospitalModel).join(
            DoctorHospitalModel,
            DoctorModel.id == DoctorHospitalModel.doctor_id
        ).filter(
            DoctorHospitalModel.hospital_id == hospital_id
        ).all()

        return [
            {
                "id": str(doctor.id),
                "name": doctor.name,
                "crm": doctor.crm,
                "specialty": doctor.specialty,
                "email": doctor.email,
                "phone": doctor.phone,
                "assigned_at": dh.created_at.isoformat()
            }
            for doctor, dh in results
        ]
