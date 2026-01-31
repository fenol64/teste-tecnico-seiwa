from abc import ABC, abstractmethod
import uuid


class IRemoveDoctorFromHospital(ABC):
    @abstractmethod
    def remove_doctor_from_hospital(self, doctor_id: uuid.UUID, hospital_id: uuid.UUID) -> bool:
        pass
