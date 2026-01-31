"""Integration tests for Doctor routes"""
import pytest
from fastapi.testclient import TestClient


class TestDoctorRoutes:
    """Integration tests for doctor endpoints"""

    def test_create_doctor_success(self, client: TestClient, auth_headers: dict, sample_doctor_data):
        """Test successful doctor creation via API"""
        response = client.post(
            "/api/v1/doctors/",
            json=sample_doctor_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_doctor_data["name"]
        assert data["crm"] == sample_doctor_data["crm"]
        assert data["email"] == sample_doctor_data["email"]
        assert "id" in data

    def test_create_doctor_unauthorized(self, client: TestClient, sample_doctor_data):
        """Test doctor creation without authentication"""
        response = client.post(
            "/api/v1/doctors/",
            json=sample_doctor_data
        )

        assert response.status_code in [401, 403]

    def test_create_doctor_duplicate_crm(self, client: TestClient, auth_headers: dict, sample_doctor_data):
        """Test doctor creation with duplicate CRM"""
        # Create first doctor
        client.post(
            "/api/v1/doctors/",
            json=sample_doctor_data,
            headers=auth_headers
        )

        # Try to create another with same CRM
        response = client.post(
            "/api/v1/doctors/",
            json=sample_doctor_data,
            headers=auth_headers
        )

        assert response.status_code == 400
        assert "Doctor with this CRM already exists." in response.json()["detail"]

    def test_get_all_doctors(self, client: TestClient, auth_headers: dict, created_doctor):
        """Test listing all doctors"""
        response = client.get(
            "/api/v1/doctors/",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_doctor_by_id(self, client: TestClient, auth_headers: dict, created_doctor):
        """Test getting doctor by ID"""
        response = client.get(
            f"/api/v1/doctors/{created_doctor.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(created_doctor.id)
        assert data["name"] == created_doctor.name

    def test_get_doctor_by_id_not_found(self, client: TestClient, auth_headers: dict):
        """Test getting non-existent doctor"""
        from uuid import uuid4

        response = client.get(
            f"/api/v1/doctors/{uuid4()}",
            headers=auth_headers
        )

        assert response.status_code == 404

    def test_update_doctor(self, client: TestClient, auth_headers: dict, created_doctor):
        """Test updating doctor"""
        update_data = {
            "name": "Dr. Updated",
            "crm": created_doctor.crm,
            "specialty": "Neurologia",
            "phone": created_doctor.phone,
            "email": created_doctor.email
        }

        response = client.put(
            f"/api/v1/doctors/{created_doctor.id}",
            json=update_data,
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Dr. Updated"
        assert data["specialty"] == "Neurologia"

    def test_delete_doctor(self, client: TestClient, auth_headers: dict, created_doctor):
        """Test deleting doctor"""
        response = client.delete(
            f"/api/v1/doctors/{created_doctor.id}",
            headers=auth_headers
        )

        assert response.status_code == 200

        # Verify doctor was deleted
        get_response = client.get(
            f"/api/v1/doctors/{created_doctor.id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404


class TestDoctorHospitalRoutes:
    """Integration tests for doctor-hospital relationship endpoints"""

    def test_assign_doctor_to_hospital(self, client: TestClient, auth_headers: dict,
                                       created_doctor, created_hospital):
        """Test assigning doctor to hospital"""
        response = client.post(
            f"/api/v1/doctors/{created_doctor.id}/hospitals/{created_hospital.id}",
            headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()
        assert data["doctor_id"] == str(created_doctor.id)
        assert data["hospital_id"] == str(created_hospital.id)

    def test_get_hospitals_by_doctor(self, client: TestClient, auth_headers: dict,
                                     created_doctor, created_hospital):
        """Test getting hospitals by doctor"""
        # First assign doctor to hospital
        client.post(
            f"/api/v1/doctors/{created_doctor.id}/hospitals/{created_hospital.id}",
            headers=auth_headers
        )

        # Get hospitals
        response = client.get(
            f"/api/v1/doctors/{created_doctor.id}/hospitals",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_remove_doctor_from_hospital(self, client: TestClient, auth_headers: dict,
                                         created_doctor, created_hospital):
        """Test removing doctor from hospital"""
        # First assign
        client.post(
            f"/api/v1/doctors/{created_doctor.id}/hospitals/{created_hospital.id}",
            headers=auth_headers
        )

        # Then remove
        response = client.delete(
            f"/api/v1/doctors/{created_doctor.id}/hospitals/{created_hospital.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
