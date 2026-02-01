from src.domain.usecase.interfaces.IGetAllHospitals import IGetAllHospitals
from typing import List, Tuple
from src.domain.entities.Hospital import Hospital


class GetAllHospitalsUseCase:
    def __init__(self, get_all_hospitals_port: IGetAllHospitals):
        self.get_all_hospitals_port = get_all_hospitals_port

    def execute(self, skip: int = 0, limit: int = 100) -> Tuple[List[Hospital], int]:
        return self.get_all_hospitals_port.get_all(skip=skip, limit=limit)
