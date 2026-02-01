"""Unit tests for repositories"""
import pytest
from uuid import uuid4
from datetime import date, datetime, timezone
from decimal import Decimal

from src.infrastructure.repositories.doctor_repository import DoctorRepository
from src.infrastructure.repositories.hospital_repository import HospitalRepository
from src.infrastructure.repositories.production_repository import ProductionRepository
from src.infrastructure.repositories.repasse_repository import RepasseRepository
from src.dto.doctorDTO import CreateDoctorDTO, UpdateDoctorDTO
from src.dto.hospitalDTO import CreateHospitalDTO, UpdateHospitalDTO
from src.dto.productionDTO import CreateProductionDTO, UpdateProductionDTO
from src.dto.repasseDTO import CreateRepasseDTO, UpdateRepasseDTO
from src.domain.entities.Doctor import Doctor
from src.domain.entities.Hospital import Hospital
from src.domain.entities.Production import Production
from src.domain.entities.Repasse import Repasse
from src.domain.enums.repasse_status import RepasseStatus


class TestDoctorRepository:
    """Test cases for DoctorRepository"""

    def test_create_doctor(self, db_session, sample_doctor_data):
        """Test creating a doctor"""
        repo = DoctorRepository(db_session)
        # Repo expects Entity, not DTO
        doctor = Doctor(
            id=uuid4(),
            name=sample_doctor_data["name"],
            crm=sample_doctor_data["crm"],
            specialty=sample_doctor_data["specialty"],
            phone=sample_doctor_data["phone"],
            email=sample_doctor_data["email"],
            created_at=datetime.now(timezone.utc).isoformat()
        )

        result = repo.save(doctor)

        assert result is not None
        assert result.name == sample_doctor_data["name"]
        assert result.crm == sample_doctor_data["crm"]
        assert result.id is not None

    def test_get_doctor_by_id(self, db_session, created_doctor):
        """Test getting doctor by ID"""
        repo = DoctorRepository(db_session)

        result = repo.get_by_id(created_doctor.id)

        assert result is not None
        assert result.id == created_doctor.id
        assert result.name == created_doctor.name

    def test_get_doctor_by_crm(self, db_session, created_doctor):
        """Test getting doctor by CRM"""
        repo = DoctorRepository(db_session)

        result = repo.get_by_crm(created_doctor.crm)

        assert result is not None
        assert result.crm == created_doctor.crm

    def test_get_doctor_by_email(self, db_session, created_doctor):
        """Test getting doctor by email"""
        repo = DoctorRepository(db_session)

        result = repo.get_by_email(created_doctor.email)

        assert result is not None
        assert result.email == created_doctor.email

    def test_get_all_doctors(self, db_session, created_doctor):
        """Test getting all doctors"""
        repo = DoctorRepository(db_session)

        doctors, total = repo.get_all()

        assert len(doctors) > 0
        assert total > 0
        assert any(d.id == created_doctor.id for d in doctors)

    def test_update_doctor(self, db_session, created_doctor):
        """Test updating a doctor"""
        repo = DoctorRepository(db_session)

        # update takes (id, **kwargs)
        result = repo.update(created_doctor.id, name="Dr. Updated")

        assert result is not None
        assert result.name == "Dr. Updated"
        assert result.id == created_doctor.id

    def test_delete_doctor(self, db_session, created_doctor):
        """Test deleting a doctor"""
        repo = DoctorRepository(db_session)

        result = repo.delete(created_doctor.id)

        assert result is True
        assert repo.get_by_id(created_doctor.id) is None


class TestHospitalRepository:
    """Test cases for HospitalRepository"""

    def test_create_hospital(self, db_session):
        """Test creating a hospital"""
        repo = HospitalRepository(db_session)
        hospital_data = {
            "name": "Hospital ABC",
            "address": "Rua X"
        }

        hospital = Hospital(
            id=uuid4(),
            name=hospital_data["name"],
            address=hospital_data["address"],
            created_at=datetime.now(timezone.utc).isoformat()
        )

        result = repo.save(hospital)

        assert result is not None
        assert result.name == hospital_data["name"]

    def test_get_all_hospitals(self, db_session, created_hospital):
        """Test listing hospitals"""
        repo = HospitalRepository(db_session)
        hospitals, total = repo.get_all()
        assert len(hospitals) > 0
        assert total > 0
        assert any(h.id == created_hospital.id for h in hospitals)

    def test_update_hospital(self, db_session, created_hospital):
        """Test updating hospital"""
        repo = HospitalRepository(db_session)

        result = repo.update(created_hospital.id, name="Updated Hospital")

        assert result is not None
        assert result.name == "Updated Hospital"


class TestProductionRepository:
    """Test cases for ProductionRepository"""

    def test_create_production(self, db_session, created_doctor, created_hospital):
        """Test creating production"""
        repo = ProductionRepository(db_session)

        # Use Entity
        production = Production(
            id=uuid4(),
            doctor_id=created_doctor.id,
            hospital_id=created_hospital.id,
            type="shift",
            date=date(2024, 1, 15),
            description="Test",
            created_at=datetime.now(timezone.utc).isoformat()
        )

        result = repo.save(production)

        assert result is not None
        assert result.type == "shift"

    def test_get_productions_by_doctor(self, db_session, created_production):
        """Test getting productions by doctor"""
        repo = ProductionRepository(db_session)
        result = repo.get_by_doctor(created_production.doctor_id)
        assert len(result) > 0


class TestRepasseRepository:
    """Test cases for RepasseRepository"""

    def test_create_repasse(self, db_session, created_production):
        """Test creating repasse"""
        repo = RepasseRepository(db_session)
        dto = CreateRepasseDTO(
            production_id=created_production.id,
            amount=Decimal("1000.00")
        )

        result = repo.create(dto)

        assert result is not None
        assert result.amount == Decimal("1000.00")
        assert result.status == RepasseStatus.PENDING

    def test_get_by_doctor_and_date_range(self, db_session, created_production):
        repo = RepasseRepository(db_session)

        # Create consolidated repasse
        dto1 = CreateRepasseDTO(
            production_id=created_production.id,
            amount=Decimal("500.00"),
            status=RepasseStatus.CONSOLIDATED
        )
        repo.create(dto1)

        # Create pending repasse
        dto2 = CreateRepasseDTO(
            production_id=created_production.id,
            amount=Decimal("300.00"),
            status=RepasseStatus.PENDING
        )
        repo.create(dto2)

        doctor_id = created_production.doctor_id

        # Test without dates
        results = repo.get_by_doctor_and_date_range(doctor_id, None, None)
        assert len(results) == 2
        assert any(r.status == RepasseStatus.CONSOLIDATED for r in results)
        assert any(r.status == RepasseStatus.PENDING for r in results)
