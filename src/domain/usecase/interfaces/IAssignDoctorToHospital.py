from abc import ABC, abstractmethod
import uuid


class IAssignDoctorToHospital(ABC):
    @abstractmethod
    def assign_doctor_to_hospital(self, doctor_id: uuid.UUID, hospital_id: uuid.UUID) -> dict:
        pass
