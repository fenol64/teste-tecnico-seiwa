from abc import ABC, abstractmethod
from typing import List
import uuid


class IGetDoctorsByHospital(ABC):
    @abstractmethod
    def get_doctors_by_hospital(self, hospital_id: uuid.UUID) -> List[dict]:
        pass
