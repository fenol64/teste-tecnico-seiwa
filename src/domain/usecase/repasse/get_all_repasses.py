from typing import List, Tuple
from src.domain.entities.Repasse import Repasse
from src.domain.usecase.interfaces.repasse_repository_interface import IRepasseRepository


class GetAllRepassesUseCase:
    def __init__(self, repasse_repository: IRepasseRepository):
        self.repasse_repository = repasse_repository

    def execute(self, skip: int = 0, limit: int = 100) -> Tuple[List[Repasse], int]:
        return self.repasse_repository.get_all(skip=skip, limit=limit)
