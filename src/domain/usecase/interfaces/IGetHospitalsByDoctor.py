from abc import ABC, abstractmethod
from typing import List
import uuid


class IGetHospitalsByDoctor(ABC):
    @abstractmethod
    def get_hospitals_by_doctor(self, doctor_id: uuid.UUID) -> List[dict]:
        pass
