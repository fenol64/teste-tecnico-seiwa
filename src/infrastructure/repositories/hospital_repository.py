from sqlalchemy.orm import Session
from typing import Optional, List, Tuple
import uuid

from src.domain.entities.Hospital import Hospital
from src.infrastructure.database.models.hospital_model import HospitalModel
from src.domain.usecase.interfaces.IGetHospitalById import IGetHospitalById
from src.domain.usecase.interfaces.ISaveHospital import ISaveHospital
from src.domain.usecase.interfaces.IUpdateHospital import IUpdateHospital
from src.domain.usecase.interfaces.IDeleteHospital import IDeleteHospital
from src.domain.usecase.interfaces.IGetAllHospitals import IGetAllHospitals


class HospitalRepository(IGetHospitalById, ISaveHospital, IUpdateHospital, IDeleteHospital, IGetAllHospitals):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, hospital_id: uuid.UUID) -> Optional[Hospital]:
        """Busca um hospital pelo ID"""
        hospital_model = self.db.query(HospitalModel).filter(HospitalModel.id == hospital_id).first()

        if not hospital_model:
            return None

        return Hospital(
            id=hospital_model.id,
            user_id=hospital_model.user_id,
            name=hospital_model.name,
            address=hospital_model.address,
            created_at=hospital_model.created_at.isoformat(),
            updated_at=hospital_model.updated_at.isoformat() if hospital_model.updated_at else None
        )

    def get_all(self, skip: int = 0, limit: int = 100, user_id: Optional[uuid.UUID] = None) -> Tuple[List[Hospital], int]:
        """Lista todos os hospitais com paginação"""
        query = self.db.query(HospitalModel)

        if user_id:
            query = query.filter(HospitalModel.user_id == user_id)

        total = query.count()
        hospitals_model = query.offset(skip).limit(limit).all()

        hospitals = [
            Hospital(
                id=hospital.id,
                user_id=hospital.user_id,
                name=hospital.name,
                address=hospital.address,
                created_at=hospital.created_at.isoformat(),
                updated_at=hospital.updated_at.isoformat() if hospital.updated_at else None
            )
            for hospital in hospitals_model
        ]

        return hospitals, total

    def save(self, hospital: Hospital) -> Hospital:
        """Salva um novo hospital no banco de dados"""
        hospital_model = HospitalModel(
            id=hospital.id,
            user_id=hospital.user_id,
            name=hospital.name,
            address=hospital.address
        )

        self.db.add(hospital_model)
        self.db.commit()
        self.db.refresh(hospital_model)

        return Hospital(
            id=hospital_model.id,
            user_id=hospital_model.user_id,
            name=hospital_model.name,
            address=hospital_model.address,
            created_at=hospital_model.created_at.isoformat(),
            updated_at=hospital_model.updated_at.isoformat() if hospital_model.updated_at else None
        )

    def update(self, hospital_id: uuid.UUID, **kwargs) -> Optional[Hospital]:
        """Atualiza os dados de um hospital"""
        hospital_model = self.db.query(HospitalModel).filter(HospitalModel.id == hospital_id).first()

        if not hospital_model:
            return None

        for key, value in kwargs.items():
            if value is not None and hasattr(hospital_model, key):
                setattr(hospital_model, key, value)

        self.db.commit()
        self.db.refresh(hospital_model)

        return Hospital(
            id=hospital_model.id,
            user_id=hospital_model.user_id,
            name=hospital_model.name,
            address=hospital_model.address,
            created_at=hospital_model.created_at.isoformat(),
            updated_at=hospital_model.updated_at.isoformat() if hospital_model.updated_at else None
        )

    def delete(self, hospital_id: uuid.UUID) -> bool:
        """Remove um hospital do banco de dados"""
        hospital_model = self.db.query(HospitalModel).filter(HospitalModel.id == hospital_id).first()

        if not hospital_model:
            return False

        self.db.delete(hospital_model)
        self.db.commit()
        return True
