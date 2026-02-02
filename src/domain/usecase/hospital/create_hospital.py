from src.domain.entities.Hospital import Hospital
from src.domain.usecase.interfaces.ISaveHospital import ISaveHospital
from src.dto.hospitalDTO import CreateHospitalDTO
import uuid
from datetime import datetime


class CreateHospitalUseCase:
    def __init__(self, save_hospital_port: ISaveHospital):
        self.save_hospital_port = save_hospital_port

    def execute(self, hospital_data: CreateHospitalDTO, user_id: uuid.UUID) -> Hospital:
        hospital_entity = Hospital(
            id=uuid.uuid4(),
            user_id=user_id,
            name=hospital_data.name,
            address=hospital_data.address,
            created_at=datetime.now().isoformat(),
        )

        return self.save_hospital_port.save(hospital_entity)
