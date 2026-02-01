from src.domain.usecase.interfaces.IGetAllDoctors import IGetAllDoctors
from typing import List, Tuple
from src.domain.entities.Doctor import Doctor


class GetAllDoctorsUseCase:
    def __init__(self, get_all_doctors_port: IGetAllDoctors):
        self.get_all_doctors_port = get_all_doctors_port

    def execute(self, skip: int = 0, limit: int = 100) -> Tuple[List[Doctor], int]:
        return self.get_all_doctors_port.get_all(skip=skip, limit=limit)
