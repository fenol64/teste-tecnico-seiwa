from uuid import UUID
from src.domain.usecase.interfaces.repasse_repository_interface import IRepasseRepository
from fastapi import HTTPException


class DeleteRepasseUseCase:
    def __init__(self, repasse_repository: IRepasseRepository):
        self.repasse_repository = repasse_repository

    def execute(self, repasse_id: UUID) -> bool:
        success = self.repasse_repository.delete(repasse_id)
        if not success:
            raise HTTPException(status_code=404, detail="Repasse not found")
        return success
