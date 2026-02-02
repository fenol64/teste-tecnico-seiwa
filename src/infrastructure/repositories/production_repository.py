from sqlalchemy.orm import Session
from typing import Optional, List, Tuple
import uuid
from datetime import date

from src.domain.entities.Production import Production
from src.infrastructure.database.models.production_model import ProductionModel
from src.domain.usecase.interfaces.IGetProductionById import IGetProductionById
from src.domain.usecase.interfaces.ISaveProduction import ISaveProduction
from src.domain.usecase.interfaces.IUpdateProduction import IUpdateProduction
from src.domain.usecase.interfaces.IDeleteProduction import IDeleteProduction
from src.domain.usecase.interfaces.IGetAllProductions import IGetAllProductions
from src.domain.usecase.interfaces.IGetProductionsByDoctor import IGetProductionsByDoctor
from src.domain.usecase.interfaces.IGetProductionsByHospital import IGetProductionsByHospital


class ProductionRepository(IGetProductionById, ISaveProduction, IUpdateProduction, IDeleteProduction, IGetAllProductions, IGetProductionsByDoctor, IGetProductionsByHospital):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, production_id: uuid.UUID) -> Optional[Production]:
        """Busca uma produção pelo ID"""
        production_model = self.db.query(ProductionModel).filter(ProductionModel.id == production_id).first()

        if not production_model:
            return None

        return Production(
            id=production_model.id,
            user_id=production_model.user_id,
            doctor_id=production_model.doctor_id,
            hospital_id=production_model.hospital_id,
            type=production_model.type.value,
            date=production_model.date,
            description=production_model.description,
            created_at=production_model.created_at.isoformat(),
            updated_at=production_model.updated_at.isoformat() if production_model.updated_at else None
        )

    def get_all(self, skip: int = 0, limit: int = 100, user_id: Optional[uuid.UUID] = None) -> Tuple[List[Production], int]:
        """Lista todas as produções com paginação"""
        query = self.db.query(ProductionModel)

        if user_id:
            query = query.filter(ProductionModel.user_id == user_id)

        total = query.count()
        productions_model = query.offset(skip).limit(limit).all()

        productions = [
            Production(
                id=production.id,
                user_id=production.user_id,
                doctor_id=production.doctor_id,
                hospital_id=production.hospital_id,
                type=production.type.value,
                date=production.date,
                description=production.description,
                created_at=production.created_at.isoformat(),
                updated_at=production.updated_at.isoformat() if production.updated_at else None
            )
            for production in productions_model
        ]

        return productions, total

    def get_by_doctor(self, doctor_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Production]:
        """Lista todas as produções de um médico específico"""
        productions_model = self.db.query(ProductionModel).filter(
            ProductionModel.doctor_id == doctor_id
        ).offset(skip).limit(limit).all()

        return [
            Production(
                id=production.id,
                user_id=production.user_id,
                doctor_id=production.doctor_id,
                hospital_id=production.hospital_id,
                type=production.type.value,
                date=production.date,
                description=production.description,
                created_at=production.created_at.isoformat(),
                updated_at=production.updated_at.isoformat() if production.updated_at else None
            )
            for production in productions_model
        ]

    def get_by_hospital(self, hospital_id: uuid.UUID) -> List[Production]:
        """Lista todas as produções de um hospital específico"""
        productions_model = self.db.query(ProductionModel).filter(
            ProductionModel.hospital_id == hospital_id
        ).all()

        return [
            Production(
                id=production.id,
                user_id=production.user_id,
                doctor_id=production.doctor_id,
                hospital_id=production.hospital_id,
                type=production.type.value,
                date=production.date,
                description=production.description,
                created_at=production.created_at.isoformat(),
                updated_at=production.updated_at.isoformat() if production.updated_at else None
            )
            for production in productions_model
        ]

    def save(self, production: Production) -> Production:
        """Salva uma nova produção no banco de dados"""
        production_model = ProductionModel(
            id=production.id,
            user_id=production.user_id,
            doctor_id=production.doctor_id,
            hospital_id=production.hospital_id,
            type=production.type,
            date=production.date,
            description=production.description
        )

        self.db.add(production_model)
        self.db.commit()
        self.db.refresh(production_model)

        return Production(
            id=production_model.id,
            user_id=production_model.user_id,
            doctor_id=production_model.doctor_id,
            hospital_id=production_model.hospital_id,
            type=production_model.type.value,
            date=production_model.date,
            description=production_model.description,
            created_at=production_model.created_at.isoformat(),
            updated_at=production_model.updated_at.isoformat() if production_model.updated_at else None
        )

    def update(self, production_id: uuid.UUID, **kwargs) -> Optional[Production]:
        """Atualiza os dados de uma produção"""
        production_model = self.db.query(ProductionModel).filter(ProductionModel.id == production_id).first()

        if not production_model:
            return None

        for key, value in kwargs.items():
            if value is not None and hasattr(production_model, key):
                setattr(production_model, key, value)

        self.db.commit()
        self.db.refresh(production_model)

        return Production(
            id=production_model.id,
            user_id=production_model.user_id,
            hospital_id=production_model.hospital_id,
            doctor_id=production_model.doctor_id,
            type=production_model.type.value,
            date=production_model.date,
            description=production_model.description,
            created_at=production_model.created_at.isoformat(),
            updated_at=production_model.updated_at.isoformat() if production_model.updated_at else None
        )

    def delete(self, production_id: uuid.UUID) -> bool:
        """Remove uma produção do banco de dados"""
        production_model = self.db.query(ProductionModel).filter(ProductionModel.id == production_id).first()

        if not production_model:
            return False

        self.db.delete(production_model)
        self.db.commit()
        return True
