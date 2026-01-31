"""Unit tests for Doctor use cases"""
import pytest
from uuid import uuid4
from unittest.mock import Mock

from src.domain.usecase.doctor.create_doctor import CreateDoctorUseCase
from src.domain.usecase.doctor.get_doctor_by_id import GetDoctorByIdUseCase
from src.domain.usecase.doctor.update_doctor import UpdateDoctorUseCase
from src.domain.usecase.doctor.delete_doctor import DeleteDoctorUseCase
from src.dto.doctorDTO import CreateDoctorDTO, UpdateDoctorDTO
from src.domain.entities.Doctor import Doctor


class TestCreateDoctorUseCase:
    """Test cases for CreateDoctorUseCase"""

    def test_create_doctor_success(self, sample_doctor_data):
        """Test successful doctor creation"""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_by_crm.return_value = None
        mock_repo.get_by_email.return_value = None
        mock_repo.save.return_value = Doctor(
            id=uuid4(),
            **sample_doctor_data,
            created_at="2024-01-01T00:00:00",
            updated_at=None
        )

        usecase = CreateDoctorUseCase(
            save_doctor_port=mock_repo,
            get_doctor_by_crm_port=mock_repo,
            get_doctor_by_email_port=mock_repo
        )

        dto = CreateDoctorDTO(**sample_doctor_data)

        # Act
        result = usecase.execute(dto)

        # Assert
        assert result is not None
        assert result.name == sample_doctor_data["name"]
        assert result.crm == sample_doctor_data["crm"]
        mock_repo.save.assert_called_once()

    def test_create_doctor_duplicate_crm(self, sample_doctor_data):
        """Test doctor creation with duplicate CRM"""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_by_crm.return_value = Doctor(
            id=uuid4(),
            **sample_doctor_data,
            created_at="2024-01-01T00:00:00",
            updated_at=None
        )

        usecase = CreateDoctorUseCase(
            save_doctor_port=mock_repo,
            get_doctor_by_crm_port=mock_repo,
            get_doctor_by_email_port=mock_repo
        )

        dto = CreateDoctorDTO(**sample_doctor_data)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            usecase.execute(dto)

        assert "Doctor with this CRM already exists." in str(exc_info.value)

    def test_create_doctor_duplicate_email(self, sample_doctor_data):
        """Test doctor creation with duplicate email"""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_by_crm.return_value = None
        mock_repo.get_by_email.return_value = Doctor(
            id=uuid4(),
            **sample_doctor_data,
            created_at="2024-01-01T00:00:00",
            updated_at=None
        )

        usecase = CreateDoctorUseCase(
            save_doctor_port=mock_repo,
            get_doctor_by_crm_port=mock_repo,
            get_doctor_by_email_port=mock_repo
        )

        dto = CreateDoctorDTO(**sample_doctor_data)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            usecase.execute(dto)

        assert "Doctor with this email already exists." in str(exc_info.value)


class TestGetDoctorByIdUseCase:
    """Test cases for GetDoctorByIdUseCase"""

    def test_get_doctor_by_id_success(self, sample_doctor_data):
        """Test successful doctor retrieval"""
        # Arrange
        doctor_id = uuid4()
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = Doctor(
            id=doctor_id,
            **sample_doctor_data,
            created_at="2024-01-01T00:00:00",
            updated_at=None
        )

        usecase = GetDoctorByIdUseCase(get_doctor_by_id_port=mock_repo)

        # Act
        result = usecase.execute(doctor_id)

        # Assert
        assert result is not None
        assert result.id == doctor_id
        mock_repo.get_by_id.assert_called_once_with(doctor_id)

    def test_get_doctor_by_id_not_found(self):
        """Test doctor retrieval when not found"""
        # Arrange
        doctor_id = uuid4()
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = None

        usecase = GetDoctorByIdUseCase(get_doctor_by_id_port=mock_repo)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            usecase.execute(doctor_id)

        assert "Doctor not found" in str(exc_info.value)


class TestUpdateDoctorUseCase:
    """Test cases for UpdateDoctorUseCase"""

    def test_update_doctor_success(self, sample_doctor_data):
        """Test successful doctor update"""
        # Arrange
        doctor_id = uuid4()
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = Doctor(
            id=doctor_id,
            **sample_doctor_data,
            created_at="2024-01-01T00:00:00",
            updated_at=None
        )

        updated_data = sample_doctor_data.copy()
        updated_data["name"] = "Dr. Updated Name"

        mock_repo.update.return_value = Doctor(
            id=doctor_id,
            **updated_data,
            created_at="2024-01-01T00:00:00",
            updated_at=None
        )

        usecase = UpdateDoctorUseCase(
            update_doctor_port=mock_repo,
            get_doctor_by_id_port=mock_repo
        )

        dto = UpdateDoctorDTO(**updated_data)

        # Act
        result = usecase.execute(doctor_id, dto)

        # Assert
        assert result is not None
        assert result.name == "Dr. Updated Name"
        mock_repo.update.assert_called_once()

    def test_update_doctor_not_found(self, sample_doctor_data):
        """Test doctor update when not found"""
        # Arrange
        doctor_id = uuid4()
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = None

        usecase = UpdateDoctorUseCase(
            update_doctor_port=mock_repo,
            get_doctor_by_id_port=mock_repo
        )

        dto = UpdateDoctorDTO(**sample_doctor_data)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            usecase.execute(doctor_id, dto)



class TestDeleteDoctorUseCase:
    """Test cases for DeleteDoctorUseCase"""

    def test_delete_doctor_success(self, sample_doctor_data):
        """Test successful doctor deletion"""
        # Arrange
        doctor_id = uuid4()
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = Doctor(
            id=doctor_id,
            **sample_doctor_data,
            created_at="2024-01-01T00:00:00",
            updated_at=None
        )
        mock_repo.delete.return_value = True

        usecase = DeleteDoctorUseCase(
            delete_doctor_port=mock_repo,
            get_doctor_by_id_port=mock_repo
        )

        # Act
        result = usecase.execute(doctor_id)

        # Assert
        assert result is True
        mock_repo.delete.assert_called_once_with(doctor_id)

    def test_delete_doctor_not_found(self):
        """Test doctor deletion when not found"""
        # Arrange
        doctor_id = uuid4()
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = None

        usecase = DeleteDoctorUseCase(
            delete_doctor_port=mock_repo,
            get_doctor_by_id_port=mock_repo
        )

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            usecase.execute(doctor_id)

