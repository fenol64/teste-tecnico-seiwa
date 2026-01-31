from src.domain.usecase.oauth.signup import SignUpUseCase
from src.domain.usecase.oauth.signin import SignInUseCase
from src.domain.usecase.doctor.create_doctor import CreateDoctorUseCase
from src.domain.usecase.doctor.get_all_doctors import GetAllDoctorsUseCase
from src.domain.usecase.doctor.get_doctor_by_id import GetDoctorByIdUseCase
from src.domain.usecase.doctor.update_doctor import UpdateDoctorUseCase
from src.domain.usecase.doctor.delete_doctor import DeleteDoctorUseCase
from src.domain.usecase.hospital.create_hospital import CreateHospitalUseCase
from src.domain.usecase.hospital.get_all_hospitals import GetAllHospitalsUseCase
from src.domain.usecase.hospital.get_hospital_by_id import GetHospitalByIdUseCase
from src.domain.usecase.hospital.update_hospital import UpdateHospitalUseCase
from src.domain.usecase.hospital.delete_hospital import DeleteHospitalUseCase
from src.domain.usecase.doctor_hospital.assign_doctor_to_hospital import AssignDoctorToHospitalUseCase
from src.domain.usecase.doctor_hospital.remove_doctor_from_hospital import RemoveDoctorFromHospitalUseCase
from src.domain.usecase.doctor_hospital.get_hospitals_by_doctor import GetHospitalsByDoctorUseCase
from src.domain.usecase.doctor_hospital.get_doctors_by_hospital import GetDoctorsByHospitalUseCase
from src.domain.usecase.production.create_production import CreateProductionUseCase
from src.domain.usecase.production.get_all_productions import GetAllProductionsUseCase
from src.domain.usecase.production.get_production_by_id import GetProductionByIdUseCase
from src.domain.usecase.production.get_productions_by_doctor import GetProductionsByDoctorUseCase
from src.domain.usecase.production.update_production import UpdateProductionUseCase
from src.domain.usecase.production.delete_production import DeleteProductionUseCase
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.repositories.doctor_repository import DoctorRepository
from src.infrastructure.repositories.hospital_repository import HospitalRepository
from src.infrastructure.repositories.doctor_hospital_repository import DoctorHospitalRepository
from src.infrastructure.repositories.production_repository import ProductionRepository
from src.infrastructure.database.connection import SessionLocal
from src.infrastructure.services.password_service import PasswordService
from src.infrastructure.services.jwt_service import JWTService
from sqlalchemy.orm import Session

class Container:
    def __init__(self, db: Session):
        self.db = db

        # Repositories
        self.user_repository = UserRepository(db=self.db)
        self.doctor_repository = DoctorRepository(db=self.db)
        self.hospital_repository = HospitalRepository(db=self.db)
        self.doctor_hospital_repository = DoctorHospitalRepository(db=self.db)
        self.production_repository = ProductionRepository(db=self.db)

        # Services
        self.password_service = PasswordService()
        self.token_service = JWTService()

        # User UseCases
        self.signup_usecase = SignUpUseCase(
            get_user_by_email_port=self.user_repository,
            encrypt_password_port=self.password_service,
            save_user_port=self.user_repository
        )

        self.signin_usecase = SignInUseCase(
            get_user_by_email_port=self.user_repository,
            encrypt_password_port=self.password_service,
            token_service_port=self.token_service
        )

        # Doctor UseCases
        self.create_doctor_usecase = CreateDoctorUseCase(
            save_doctor_port=self.doctor_repository,
            get_doctor_by_crm_port=self.doctor_repository,
            get_doctor_by_email_port=self.doctor_repository
        )

        self.get_all_doctors_usecase = GetAllDoctorsUseCase(
            get_all_doctors_port=self.doctor_repository
        )

        self.get_doctor_by_id_usecase = GetDoctorByIdUseCase(
            get_doctor_by_id_port=self.doctor_repository
        )

        self.update_doctor_usecase = UpdateDoctorUseCase(
            update_doctor_port=self.doctor_repository,
            get_doctor_by_id_port=self.doctor_repository
        )

        self.delete_doctor_usecase = DeleteDoctorUseCase(
            delete_doctor_port=self.doctor_repository,
            get_doctor_by_id_port=self.doctor_repository
        )

        # Hospital UseCases
        self.create_hospital_usecase = CreateHospitalUseCase(
            save_hospital_port=self.hospital_repository
        )

        self.get_all_hospitals_usecase = GetAllHospitalsUseCase(
            get_all_hospitals_port=self.hospital_repository
        )

        self.get_hospital_by_id_usecase = GetHospitalByIdUseCase(
            get_hospital_by_id_port=self.hospital_repository
        )

        self.update_hospital_usecase = UpdateHospitalUseCase(
            update_hospital_port=self.hospital_repository,
            get_hospital_by_id_port=self.hospital_repository
        )

        self.delete_hospital_usecase = DeleteHospitalUseCase(
            delete_hospital_port=self.hospital_repository,
            get_hospital_by_id_port=self.hospital_repository
        )

        # Doctor-Hospital UseCases
        self.assign_doctor_to_hospital_usecase = AssignDoctorToHospitalUseCase(
            assign_doctor_to_hospital_port=self.doctor_hospital_repository,
            get_doctor_by_id_port=self.doctor_repository,
            get_hospital_by_id_port=self.hospital_repository
        )

        self.remove_doctor_from_hospital_usecase = RemoveDoctorFromHospitalUseCase(
            remove_doctor_from_hospital_port=self.doctor_hospital_repository
        )

        self.get_hospitals_by_doctor_usecase = GetHospitalsByDoctorUseCase(
            get_hospitals_by_doctor_port=self.doctor_hospital_repository
        )

        self.get_doctors_by_hospital_usecase = GetDoctorsByHospitalUseCase(
            get_doctors_by_hospital_port=self.doctor_hospital_repository
        )

        # Production UseCases
        self.create_production_usecase = CreateProductionUseCase(
            save_production_port=self.production_repository,
            get_doctor_by_id_port=self.doctor_repository
        )

        self.get_all_productions_usecase = GetAllProductionsUseCase(
            get_all_productions_port=self.production_repository
        )

        self.get_production_by_id_usecase = GetProductionByIdUseCase(
            get_production_by_id_port=self.production_repository
        )

        self.get_productions_by_doctor_usecase = GetProductionsByDoctorUseCase(
            get_productions_by_doctor_port=self.production_repository
        )

        self.update_production_usecase = UpdateProductionUseCase(
            update_production_port=self.production_repository,
            get_production_by_id_port=self.production_repository
        )

        self.delete_production_usecase = DeleteProductionUseCase(
            delete_production_port=self.production_repository,
            get_production_by_id_port=self.production_repository
        )


