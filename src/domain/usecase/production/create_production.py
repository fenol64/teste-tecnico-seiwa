from src.domain.entities.Production import Production
from src.domain.usecase.interfaces.ISaveProduction import ISaveProduction
from src.domain.usecase.interfaces.IGetDoctorById import IGetDoctorById
from src.dto.productionDTO import CreateProductionDTO
import uuid
from datetime import datetime


class CreateProductionUseCase:
    def __init__(
        self,
        save_production_port: ISaveProduction,
        get_doctor_by_id_port: IGetDoctorById
    ):
        self.save_production_port = save_production_port
        self.get_doctor_by_id_port = get_doctor_by_id_port

    def execute(self, production_data: CreateProductionDTO) -> Production:
        # Verifica se o médico existe
        doctor = self.get_doctor_by_id_port.get_by_id(uuid.UUID(production_data.doctor_id))
        if not doctor:
            raise ValueError("Doctor not found.")

        production_entity = Production(
            id=uuid.uuid4(),
            doctor_id=uuid.UUID(production_data.doctor_id),
            type=production_data.type.value,
            date=production_data.date,
            description=production_data.description,
            created_at=datetime.now().isoformat(),
        )

        return self.save_production_port.save(production_entity)
