from src.domain.usecase.interfaces.IGetAllHospitals import IGetAllHospitals
from typing import List, Tuple, Optional
from src.domain.entities.Hospital import Hospital
import uuid


class GetAllHospitalsUseCase:
    def __init__(self, get_all_hospitals_port: IGetAllHospitals):
        self.get_all_hospitals_port = get_all_hospitals_port

    def execute(self, skip: int = 0, limit: int = 100, user_id: Optional[uuid.UUID] = None) -> Tuple[List[Hospital], int]:
        return self.get_all_hospitals_port.get_all(skip=skip, limit=limit, user_id=user_id)
