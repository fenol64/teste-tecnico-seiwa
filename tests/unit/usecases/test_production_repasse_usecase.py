"""Unit tests for Production use cases"""
import pytest
from uuid import uuid4
from unittest.mock import Mock
from datetime import date
from decimal import Decimal
from fastapi import HTTPException

from src.domain.usecase.production.create_production import CreateProductionUseCase
from src.domain.usecase.repasse.create_repasse import CreateRepasseUseCase
from src.dto.productionDTO import CreateProductionDTO
from src.dto.repasseDTO import CreateRepasseDTO
from src.domain.entities.Production import Production
from src.domain.entities.Repasse import Repasse
from src.domain.entities.Doctor import Doctor
from src.domain.entities.Hospital import Hospital


class TestCreateProductionUseCase:
    """Test cases for CreateProductionUseCase"""

    def test_create_production_success(self, sample_doctor_data, sample_hospital_data):
        """Test successful production creation"""
        # Arrange
        doctor_id = uuid4()
        hospital_id = uuid4()

        mock_production_repo = Mock()
        mock_doctor_repo = Mock()
        mock_hospital_repo = Mock()

        mock_doctor_repo.get_by_id.return_value = Doctor(
            id=doctor_id,
            **sample_doctor_data,
            created_at="2024-01-01T00:00:00",
            updated_at=None
        )

        mock_hospital_repo.get_by_id.return_value = Hospital(
            id=hospital_id,
            name="Hospital Test",
            address="Test Address",
            created_at="2024-01-01T00:00:00",
            updated_at=None
        )

        mock_production_repo.save.return_value = Production(
            id=uuid4(),
            doctor_id=str(doctor_id),
            hospital_id=str(hospital_id),
            type="plantao",
            date=date(2024, 1, 15),
            description="Test",
            created_at="2024-01-01T00:00:00",
            updated_at=None
        )

        usecase = CreateProductionUseCase(
            save_production_port=mock_production_repo,
            get_doctor_by_id_port=mock_doctor_repo,
            get_hospital_by_id_port=mock_hospital_repo
        )

        dto = CreateProductionDTO(
            doctor_id=str(doctor_id),
            hospital_id=str(hospital_id),
            type="plantao",
            date=date(2024, 1, 15),
            description="Test"
        )

        # Act
        result = usecase.execute(dto)

        # Assert
        assert result is not None
        assert result.doctor_id == doctor_id
        assert result.hospital_id == hospital_id
        mock_production_repo.save.assert_called_once()

    def test_create_production_doctor_not_found(self):
        """Test production creation with non-existent doctor"""
        # Arrange
        doctor_id = uuid4()
        hospital_id = uuid4()

        mock_production_repo = Mock()
        mock_doctor_repo = Mock()
        mock_hospital_repo = Mock()

        mock_doctor_repo.get_by_id.return_value = None

        usecase = CreateProductionUseCase(
            save_production_port=mock_production_repo,
            get_doctor_by_id_port=mock_doctor_repo,
            get_hospital_by_id_port=mock_hospital_repo
        )

        dto = CreateProductionDTO(
            doctor_id=str(doctor_id),
            hospital_id=str(hospital_id),
            type="plantao",
            date=date(2024, 1, 15),
            description="Test"
        )

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            usecase.execute(dto)

        assert "Doctor not found" in str(exc_info.value)

    def test_create_production_hospital_not_found(self, sample_doctor_data):
        """Test production creation with non-existent hospital"""
        # Arrange
        doctor_id = uuid4()
        hospital_id = uuid4()

        mock_production_repo = Mock()
        mock_doctor_repo = Mock()
        mock_hospital_repo = Mock()

        mock_doctor_repo.get_by_id.return_value = Doctor(
            id=doctor_id,
            **sample_doctor_data,
            created_at="2024-01-01T00:00:00",
            updated_at=None
        )

        mock_hospital_repo.get_by_id.return_value = None

        usecase = CreateProductionUseCase(
            save_production_port=mock_production_repo,
            get_doctor_by_id_port=mock_doctor_repo,
            get_hospital_by_id_port=mock_hospital_repo
        )

        dto = CreateProductionDTO(
            doctor_id=str(doctor_id),
            hospital_id=str(hospital_id),
            type="plantao",
            date=date(2024, 1, 15),
            description="Test"
        )

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            usecase.execute(dto)

        assert "Hospital not found" in str(exc_info.value)


class TestCreateRepasseUseCase:
    """Test cases for CreateRepasseUseCase"""

    def test_create_repasse_success(self):
        """Test successful repasse creation"""
        # Arrange
        production_id = uuid4()

        mock_repasse_repo = Mock()
        mock_production_repo = Mock()

        mock_production_repo.get_by_id.return_value = Production(
            id=production_id,
            doctor_id=uuid4(),
            hospital_id=uuid4(),
            type="plantao",
            date=date(2024, 1, 15),
            description="Test",
            created_at="2024-01-01T00:00:00",
            updated_at=None
        )

        mock_repasse_repo.create.return_value = Repasse(
            id=uuid4(),
            production_id=production_id,
            valor=Decimal("1500.00"),
            created_at="2024-01-01T00:00:00",
            updated_at=None
        )

        usecase = CreateRepasseUseCase(
            repasse_repository=mock_repasse_repo,
            production_repository=mock_production_repo
        )

        dto = CreateRepasseDTO(
            production_id=production_id,
            valor=Decimal("1500.00")
        )

        # Act
        result = usecase.execute(dto)

        # Assert
        assert result is not None
        assert result.production_id == production_id
        assert result.valor == Decimal("1500.00")
        mock_repasse_repo.create.assert_called_once()

    def test_create_repasse_production_not_found(self):
        """Test repasse creation with non-existent production"""
        # Arrange
        production_id = uuid4()

        mock_repasse_repo = Mock()
        mock_production_repo = Mock()

        mock_production_repo.get_by_id.return_value = None

        usecase = CreateRepasseUseCase(
            repasse_repository=mock_repasse_repo,
            production_repository=mock_production_repo
        )

        dto = CreateRepasseDTO(
            production_id=production_id,
            valor=Decimal("1500.00")
        )

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            usecase.execute(dto)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Production not found"
