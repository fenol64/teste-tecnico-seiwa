from uuid import UUID
from src.domain.entities.Repasse import Repasse
from src.domain.usecase.interfaces.repasse_repository_interface import IRepasseRepository
from fastapi import HTTPException


class GetRepasseByIdUseCase:
    def __init__(self, repasse_repository: IRepasseRepository):
        self.repasse_repository = repasse_repository

    def execute(self, repasse_id: UUID) -> Repasse:
        repasse = self.repasse_repository.get_by_id(repasse_id)
        if not repasse:
            raise HTTPException(status_code=404, detail="Repasse not found")
        return repasse
