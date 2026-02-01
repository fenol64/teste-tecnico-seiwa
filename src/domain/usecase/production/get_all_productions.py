from src.domain.usecase.interfaces.IGetAllProductions import IGetAllProductions
from typing import List, Tuple
from src.domain.entities.Production import Production


class GetAllProductionsUseCase:
    def __init__(self, get_all_productions_port: IGetAllProductions):
        self.get_all_productions_port = get_all_productions_port

    def execute(self, skip: int = 0, limit: int = 100) -> Tuple[List[Production], int]:
        return self.get_all_productions_port.get_all(skip=skip, limit=limit)
