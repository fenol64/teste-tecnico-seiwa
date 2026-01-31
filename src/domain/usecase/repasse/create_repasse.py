from src.domain.entities.Repasse import Repasse
from src.dto.repasseDTO import CreateRepasseDTO
from src.domain.usecase.interfaces.repasse_repository_interface import IRepasseRepository
from src.domain.usecase.interfaces.IGetProductionById import IGetProductionById
from fastapi import HTTPException


class CreateRepasseUseCase:
    def __init__(
        self,
        repasse_repository: IRepasseRepository,
        production_repository: IGetProductionById
    ):
        self.repasse_repository = repasse_repository
        self.production_repository = production_repository

    def execute(self, data: CreateRepasseDTO) -> Repasse:
        # Valida se a produção existe
        production = self.production_repository.get_by_id(data.production_id)
        if not production:
            raise HTTPException(status_code=404, detail="Production not found")

        return self.repasse_repository.create(data)
