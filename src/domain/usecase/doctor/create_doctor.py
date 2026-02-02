from src.domain.entities.Doctor import Doctor
from src.domain.usecase.interfaces.ISaveDoctor import ISaveDoctor
from src.domain.usecase.interfaces.IGetDoctorByCRM import IGetDoctorByCRM
from src.domain.usecase.interfaces.IGetDoctorByEmail import IGetDoctorByEmail
from src.dto.doctorDTO import CreateDoctorDTO
import uuid
from datetime import datetime


class CreateDoctorUseCase:
    def __init__(
        self,
        save_doctor_port: ISaveDoctor,
        get_doctor_by_crm_port: IGetDoctorByCRM,
        get_doctor_by_email_port: IGetDoctorByEmail
    ):
        self.save_doctor_port = save_doctor_port
        self.get_doctor_by_crm_port = get_doctor_by_crm_port
        self.get_doctor_by_email_port = get_doctor_by_email_port

    def execute(self, doctor_data: CreateDoctorDTO, user_id: uuid.UUID) -> Doctor:
        # Verifica se já existe médico com este CRM
        existing_crm = self.get_doctor_by_crm_port.get_by_crm(doctor_data.crm)
        if existing_crm:
            raise ValueError("Doctor with this CRM already exists.")

        # Verifica se já existe médico com este email
        existing_email = self.get_doctor_by_email_port.get_by_email(doctor_data.email)
        if existing_email:
            raise ValueError("Doctor with this email already exists.")

        doctor_entity = Doctor(
            id=uuid.uuid4(),
            user_id=user_id,
            name=doctor_data.name,
            crm=doctor_data.crm,
            specialty=doctor_data.specialty,
            phone=doctor_data.phone,
            email=doctor_data.email,
            created_at=datetime.now().isoformat(),
        )

        return self.save_doctor_port.save(doctor_entity)
