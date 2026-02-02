from src.domain.usecase.interfaces.IGetAllDoctors import IGetAllDoctors
from typing import List, Tuple, Optional
from src.domain.entities.Doctor import Doctor
import uuid


class GetAllDoctorsUseCase:
    def __init__(self, get_all_doctors_port: IGetAllDoctors):
        self.get_all_doctors_port = get_all_doctors_port

    def execute(self, skip: int = 0, limit: int = 100, user_id: Optional[uuid.UUID] = None) -> Tuple[List[Doctor], int]:
        return self.get_all_doctors_port.get_all(skip=skip, limit=limit, user_id=user_id)
