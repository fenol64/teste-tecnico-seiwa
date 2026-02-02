from sqlalchemy.orm import Session
from typing import Optional, List, Tuple
import uuid

from src.domain.entities.Doctor import Doctor
from src.infrastructure.database.models.doctor_model import DoctorModel
from src.domain.usecase.interfaces.IGetDoctorById import IGetDoctorById
from src.domain.usecase.interfaces.IGetDoctorByCRM import IGetDoctorByCRM
from src.domain.usecase.interfaces.IGetDoctorByEmail import IGetDoctorByEmail
from src.domain.usecase.interfaces.ISaveDoctor import ISaveDoctor
from src.domain.usecase.interfaces.IUpdateDoctor import IUpdateDoctor
from src.domain.usecase.interfaces.IDeleteDoctor import IDeleteDoctor
from src.domain.usecase.interfaces.IGetAllDoctors import IGetAllDoctors


class DoctorRepository(IGetDoctorById, IGetDoctorByCRM, IGetDoctorByEmail, ISaveDoctor, IUpdateDoctor, IDeleteDoctor, IGetAllDoctors):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, doctor_id: uuid.UUID) -> Optional[Doctor]:
        """Busca um médico pelo ID"""
        doctor_model = self.db.query(DoctorModel).filter(DoctorModel.id == doctor_id).first()

        if not doctor_model:
            return None

        return Doctor(
            id=doctor_model.id,
            user_id=doctor_model.user_id,
            name=doctor_model.name,
            crm=doctor_model.crm,
            specialty=doctor_model.specialty,
            phone=doctor_model.phone,
            email=doctor_model.email,
            created_at=doctor_model.created_at.isoformat(),
            updated_at=doctor_model.updated_at.isoformat() if doctor_model.updated_at else None
        )

    def get_by_crm(self, crm: str) -> Optional[Doctor]:
        """Busca um médico pelo CRM"""
        doctor_model = self.db.query(DoctorModel).filter(DoctorModel.crm == crm).first()

        if not doctor_model:
            return None

        return Doctor(
            id=doctor_model.id,
            user_id=doctor_model.user_id,
            name=doctor_model.name,
            crm=doctor_model.crm,
            specialty=doctor_model.specialty,
            phone=doctor_model.phone,
            email=doctor_model.email,
            created_at=doctor_model.created_at.isoformat(),
            updated_at=doctor_model.updated_at.isoformat() if doctor_model.updated_at else None
        )

    def get_by_email(self, email: str) -> Optional[Doctor]:
        """Busca um médico pelo email"""
        doctor_model = self.db.query(DoctorModel).filter(DoctorModel.email == email).first()

        if not doctor_model:
            return None

        return Doctor(
            id=doctor_model.id,
            user_id=doctor_model.user_id,
            name=doctor_model.name,
            crm=doctor_model.crm,
            specialty=doctor_model.specialty,
            phone=doctor_model.phone,
            email=doctor_model.email,
            created_at=doctor_model.created_at.isoformat(),
            updated_at=doctor_model.updated_at.isoformat() if doctor_model.updated_at else None
        )

    def get_all(self, skip: int = 0, limit: int = 100, user_id: Optional[uuid.UUID] = None) -> Tuple[List[Doctor], int]:
        """Lista todos os médicos com paginação"""
        query = self.db.query(DoctorModel)

        if user_id:
            query = query.filter(DoctorModel.user_id == user_id)

        total = query.count()
        doctors_model = query.offset(skip).limit(limit).all()

        doctors = [
            Doctor(
                id=doctor.id,
                user_id=doctor.user_id,
                name=doctor.name,
                crm=doctor.crm,
                specialty=doctor.specialty,
                phone=doctor.phone,
                email=doctor.email,
                created_at=doctor.created_at.isoformat(),
                updated_at=doctor.updated_at.isoformat() if doctor.updated_at else None
            )
            for doctor in doctors_model
        ]

        return doctors, total

    def save(self, doctor: Doctor) -> Doctor:
        """Salva um novo médico no banco de dados"""
        doctor_model = DoctorModel(
            id=doctor.id,
            user_id=doctor.user_id,
            name=doctor.name,
            crm=doctor.crm,
            specialty=doctor.specialty,
            phone=doctor.phone,
            email=doctor.email
        )

        self.db.add(doctor_model)
        self.db.commit()
        self.db.refresh(doctor_model)

        return Doctor(
            id=doctor_model.id,
            user_id=doctor_model.user_id,
            name=doctor_model.name,
            crm=doctor_model.crm,
            specialty=doctor_model.specialty,
            phone=doctor_model.phone,
            email=doctor_model.email,
            created_at=doctor_model.created_at.isoformat(),
            updated_at=doctor_model.updated_at.isoformat() if doctor_model.updated_at else None
        )

    def update(self, doctor_id: uuid.UUID, **kwargs) -> Optional[Doctor]:
        """Atualiza os dados de um médico"""
        doctor_model = self.db.query(DoctorModel).filter(DoctorModel.id == doctor_id).first()

        if not doctor_model:
            return None

        for key, value in kwargs.items():
            if value is not None and hasattr(doctor_model, key):
                setattr(doctor_model, key, value)

        self.db.commit()
        self.db.refresh(doctor_model)

        return Doctor(
            id=doctor_model.id,
            user_id=doctor_model.user_id,
            name=doctor_model.name,
            crm=doctor_model.crm,
            specialty=doctor_model.specialty,
            phone=doctor_model.phone,
            email=doctor_model.email,
            created_at=doctor_model.created_at.isoformat(),
            updated_at=doctor_model.updated_at.isoformat() if doctor_model.updated_at else None
        )

    def delete(self, doctor_id: uuid.UUID) -> bool:
        """Remove um médico do banco de dados"""
        doctor_model = self.db.query(DoctorModel).filter(DoctorModel.id == doctor_id).first()

        if not doctor_model:
            return False

        self.db.delete(doctor_model)
        self.db.commit()
        return True
