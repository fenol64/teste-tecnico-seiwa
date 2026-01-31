"""Integration tests for Hospital routes"""
import pytest
from fastapi.testclient import TestClient


class TestHospitalRoutes:
    """Integration tests for hospital endpoints"""

    def test_create_hospital_success(self, client: TestClient, auth_headers: dict):
        """Test successful hospital creation"""
        hospital_data = {
            "name": "Hospital Central",
            "address": "Av. Principal, 1000"
        }

        response = client.post(
            "/api/v1/hospitals/",
            json=hospital_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == hospital_data["name"]
        assert data["address"] == hospital_data["address"]
        assert "id" in data

    def test_create_hospital_unauthorized(self, client: TestClient):
        """Test hospital creation without authentication"""
        hospital_data = {
            "name": "Hospital Test",
            "address": "Test Address"
        }

        response = client.post(
            "/api/v1/hospitals/",
            json=hospital_data
        )

        assert response.status_code in [401, 403]

    def test_get_all_hospitals(self, client: TestClient, auth_headers: dict, created_hospital):
        """Test listing all hospitals"""
        response = client.get(
            "/api/v1/hospitals/",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_hospital_by_id(self, client: TestClient, auth_headers: dict, created_hospital):
        """Test getting hospital by ID"""
        response = client.get(
            f"/api/v1/hospitals/{created_hospital.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(created_hospital.id)
        assert data["name"] == created_hospital.name

    def test_get_hospital_by_id_not_found(self, client: TestClient, auth_headers: dict):
        """Test getting non-existent hospital"""
        from uuid import uuid4

        response = client.get(
            f"/api/v1/hospitals/{uuid4()}",
            headers=auth_headers
        )

        assert response.status_code == 404

    def test_update_hospital(self, client: TestClient, auth_headers: dict, created_hospital):
        """Test updating hospital"""
        update_data = {
            "name": "Hospital Updated",
            "address": "New Address, 999"
        }

        response = client.put(
            f"/api/v1/hospitals/{created_hospital.id}",
            json=update_data,
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Hospital Updated"
        assert data["address"] == "New Address, 999"

    def test_delete_hospital(self, client: TestClient, auth_headers: dict, created_hospital):
        """Test deleting hospital"""
        response = client.delete(
            f"/api/v1/hospitals/{created_hospital.id}",
            headers=auth_headers
        )

        assert response.status_code == 200

        # Verify hospital was deleted
        get_response = client.get(
            f"/api/v1/hospitals/{created_hospital.id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404

    def test_get_doctors_by_hospital(self, client: TestClient, auth_headers: dict,
                                     created_doctor, created_hospital):
        """Test getting doctors by hospital"""
        # First assign doctor to hospital
        client.post(
            f"/api/v1/doctors/{created_doctor.id}/hospitals/{created_hospital.id}",
            headers=auth_headers
        )

        # Get doctors
        response = client.get(
            f"/api/v1/hospitals/{created_hospital.id}/doctors",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
