from src.domain.usecase.interfaces.IGetAllProductions import IGetAllProductions
from typing import List, Tuple, Optional
from src.domain.entities.Production import Production
import uuid


class GetAllProductionsUseCase:
    def __init__(self, get_all_productions_port: IGetAllProductions):
        self.get_all_productions_port = get_all_productions_port

    def execute(self, skip: int = 0, limit: int = 100, user_id: Optional[uuid.UUID] = None) -> Tuple[List[Production], int]:
        return self.get_all_productions_port.get_all(skip=skip, limit=limit, user_id=user_id)
