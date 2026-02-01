from typing import List, Optional, Tuple
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from src.infrastructure.database.models.repasse_model import RepasseModel
from src.infrastructure.database.models.production_model import ProductionModel
from src.domain.entities.Repasse import Repasse
from src.dto.repasseDTO import CreateRepasseDTO, UpdateRepasseDTO
from src.domain.usecase.interfaces.repasse_repository_interface import IRepasseRepository


class RepasseRepository(IRepasseRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: CreateRepasseDTO) -> Repasse:
        repasse = RepasseModel(
            production_id=data.production_id,
            valor=data.valor,
            status=data.status
        )
        self.db.add(repasse)
        self.db.commit()
        self.db.refresh(repasse)
        return self._to_entity(repasse)

    def get_all(self, skip: int = 0, limit: int = 100) -> Tuple[List[Repasse], int]:
        query = self.db.query(RepasseModel)
        total = query.count()
        repasses = query.offset(skip).limit(limit).all()
        return [self._to_entity(repasse) for repasse in repasses], total

    def get_by_id(self, repasse_id: UUID) -> Optional[Repasse]:
        repasse = self.db.query(RepasseModel).filter(RepasseModel.id == repasse_id).first()
        return self._to_entity(repasse) if repasse else None

    def update(self, repasse_id: UUID, data: UpdateRepasseDTO) -> Optional[Repasse]:
        repasse = self.db.query(RepasseModel).filter(RepasseModel.id == repasse_id).first()
        if not repasse:
            return None

        if data.valor is not None:
            repasse.valor = data.valor
        if data.status is not None:
            repasse.status = data.status

        self.db.commit()
        self.db.refresh(repasse)
        return self._to_entity(repasse)

    def delete(self, repasse_id: UUID) -> bool:
        repasse = self.db.query(RepasseModel).filter(RepasseModel.id == repasse_id).first()
        if not repasse:
            return False

        self.db.delete(repasse)
        self.db.commit()
        return True

    def get_by_production(self, production_id: UUID) -> List[Repasse]:
        repasses = self.db.query(RepasseModel).filter(RepasseModel.production_id == production_id).all()
        return [self._to_entity(repasse) for repasse in repasses]

    def get_by_doctor_and_date_range(
        self,
        doctor_id: UUID,
        start_date: Optional[datetime],
        end_date: Optional[datetime]
    ) -> List[Repasse]:
        query = self.db.query(RepasseModel).join(ProductionModel, RepasseModel.production_id == ProductionModel.id)
        query = query.filter(ProductionModel.doctor_id == doctor_id)

        if start_date:
            query = query.filter(RepasseModel.created_at >= start_date)
        if end_date:
            query = query.filter(RepasseModel.created_at <= end_date)

        repasses = query.all()
        return [self._to_entity(repasse) for repasse in repasses]

    def _to_entity(self, model: RepasseModel) -> Repasse:
        return Repasse(
            id=model.id,
            production_id=model.production_id,
            valor=model.valor,
            created_at=model.created_at,
            updated_at=model.updated_at,
            status=model.status
        )
