from typing import List
from src.domain.entities.Repasse import Repasse
from src.domain.usecase.interfaces.repasse_repository_interface import IRepasseRepository


class GetAllRepassesUseCase:
    def __init__(self, repasse_repository: IRepasseRepository):
        self.repasse_repository = repasse_repository

    def execute(self) -> List[Repasse]:
        return self.repasse_repository.get_all()
