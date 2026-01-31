import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from typing import Generator
import uuid
from decimal import Decimal

from src.infrastructure.database.connection import Base
from src.infrastructure.database.models.user_model import UserModel
from src.infrastructure.database.models.doctor_model import DoctorModel
from src.infrastructure.database.models.hospital_model import HospitalModel
from src.infrastructure.database.models.doctor_hospital_model import DoctorHospitalModel
from src.infrastructure.database.models.production_model import ProductionModel
from src.infrastructure.database.models.repasse_model import RepasseModel
from main import create_app
from src.infrastructure.services.password_service import PasswordService


# Database fixture for tests
@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Create a fresh database session for each test"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Create a test client with database dependency override"""
    from src.infrastructure.database.connection import get_db

    app = create_app()

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def password_service() -> PasswordService:
    """Password service fixture"""
    return PasswordService()


@pytest.fixture
def sample_user_data():
    """Sample user data for tests"""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "password": "Test@1234"
    }


@pytest.fixture
def sample_doctor_data():
    """Sample doctor data for tests"""
    return {
        "name": "Dr. John Doe",
        "crm": "123456",
        "specialty": "Cardiologia",
        "phone": "11999999999",
        "email": "doctor@example.com"
    }


@pytest.fixture
def sample_hospital_data():
    """Sample hospital data for tests"""
    return {
        "name": "Hospital Test",
        "address": "Rua Teste, 123"
    }


@pytest.fixture
def sample_production_data():
    """Sample production data for tests"""
    return {
        "type": "plantao",
        "date": "2024-01-15",
        "description": "Plantão noturno"
    }


@pytest.fixture
def sample_repasse_data():
    """Sample repasse data for tests"""
    return {
        "valor": Decimal("1500.00")
    }


@pytest.fixture
def created_user(db_session: Session, password_service: PasswordService):
    """Create a user in the database"""
    hashed_password = password_service.encrypt_password("Test@1234")
    user = UserModel(
        name="Test User",
        email="test@example.com",
        password=hashed_password
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_token(client: TestClient, created_user: UserModel) -> str:
    """Get authentication token"""
    response = client.post(
        "/api/v1/signin",
        json={
            "email": "test@example.com",
            "password": "Test@1234"
        }
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token: str) -> dict:
    """Get authorization headers"""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def created_doctor(db_session: Session):
    """Create a doctor in the database"""
    doctor = DoctorModel(
        name="Dr. Test",
        crm="123456",
        specialty="Cardiologia",
        phone="11999999999",
        email="doctor@test.com"
    )
    db_session.add(doctor)
    db_session.commit()
    db_session.refresh(doctor)
    return doctor


@pytest.fixture
def created_hospital(db_session: Session):
    """Create a hospital in the database"""
    hospital = HospitalModel(
        name="Hospital Test",
        address="Rua Test, 123"
    )
    db_session.add(hospital)
    db_session.commit()
    db_session.refresh(hospital)
    return hospital


@pytest.fixture
def created_production(db_session: Session, created_doctor: DoctorModel, created_hospital: HospitalModel):
    """Create a production in the database"""
    from datetime import date
    from src.infrastructure.database.models.production_model import ProductionType

    production = ProductionModel(
        doctor_id=created_doctor.id,
        hospital_id=created_hospital.id,
        type=ProductionType.PLANTAO,
        date=date(2024, 1, 15),
        description="Test production"
    )
    db_session.add(production)
    db_session.commit()
    db_session.refresh(production)
    return production
