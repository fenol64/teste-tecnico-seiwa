from src.domain.usecase.interfaces.IDeleteHospital import IDeleteHospital
from src.domain.usecase.interfaces.IGetHospitalById import IGetHospitalById
import uuid


class DeleteHospitalUseCase:
    def __init__(
        self,
        delete_hospital_port: IDeleteHospital,
        get_hospital_by_id_port: IGetHospitalById
    ):
        self.delete_hospital_port = delete_hospital_port
        self.get_hospital_by_id_port = get_hospital_by_id_port

    def execute(self, hospital_id: uuid.UUID) -> bool:
        # Verifica se o hospital existe
        existing_hospital = self.get_hospital_by_id_port.get_by_id(hospital_id)
        if not existing_hospital:
            raise ValueError("Hospital not found.")

        return self.delete_hospital_port.delete(hospital_id)
