from src.domain.usecase.interfaces.IGetAllDoctors import IGetAllDoctors
from typing import List
from src.domain.entities.Doctor import Doctor


class GetAllDoctorsUseCase:
    def __init__(self, get_all_doctors_port: IGetAllDoctors):
        self.get_all_doctors_port = get_all_doctors_port

    def execute(self, skip: int = 0, limit: int = 100) -> List[Doctor]:
        return self.get_all_doctors_port.get_all(skip=skip, limit=limit)
