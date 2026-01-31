from src.domain.usecase.interfaces.IUpdateHospital import IUpdateHospital
from src.domain.usecase.interfaces.IGetHospitalById import IGetHospitalById
from src.dto.hospitalDTO import UpdateHospitalDTO
from typing import Optional
import uuid
from src.domain.entities.Hospital import Hospital


class UpdateHospitalUseCase:
    def __init__(
        self,
        update_hospital_port: IUpdateHospital,
        get_hospital_by_id_port: IGetHospitalById
    ):
        self.update_hospital_port = update_hospital_port
        self.get_hospital_by_id_port = get_hospital_by_id_port

    def execute(self, hospital_id: uuid.UUID, hospital_data: UpdateHospitalDTO) -> Optional[Hospital]:
        # Verifica se o hospital existe
        existing_hospital = self.get_hospital_by_id_port.get_by_id(hospital_id)
        if not existing_hospital:
            raise ValueError("Hospital not found.")

        # Prepara dados para atualização (apenas campos não nulos)
        update_data = {k: v for k, v in hospital_data.model_dump().items() if v is not None}

        if not update_data:
            return existing_hospital

        updated_hospital = self.update_hospital_port.update(hospital_id, **update_data)
        return updated_hospital
