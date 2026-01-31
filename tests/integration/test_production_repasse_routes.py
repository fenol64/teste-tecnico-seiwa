"""Integration tests for Production and Repasse routes"""
import pytest
from fastapi.testclient import TestClient
from uuid import uuid4


class TestProductionRoutes:
    """Integration tests for production endpoints"""

    def test_create_production_success(self, client: TestClient, auth_headers: dict,
                                       created_doctor, created_hospital):
        """Test successful production creation"""
        production_data = {
            "doctor_id": str(created_doctor.id),
            "hospital_id": str(created_hospital.id),
            "type": "plantao",
            "date": "2024-01-15",
            "description": "Plantão noturno"
        }

        response = client.post(
            "/api/v1/productions/",
            json=production_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()
        assert data["doctor_id"] == str(created_doctor.id)
        assert data["hospital_id"] == str(created_hospital.id)
        assert data["type"] == "plantao"

    def test_create_production_invalid_doctor(self, client: TestClient, auth_headers: dict,
                                              created_hospital):
        """Test production creation with invalid doctor"""
        production_data = {
            "doctor_id": str(uuid4()),
            "hospital_id": str(created_hospital.id),
            "type": "plantao",
            "date": "2024-01-15",
            "description": "Test"
        }

        response = client.post(
            "/api/v1/productions/",
            json=production_data,
            headers=auth_headers
        )

        assert response.status_code == 404
        assert "Doctor not found" in response.json()["detail"]

    def test_create_production_invalid_hospital(self, client: TestClient, auth_headers: dict,
                                                created_doctor):
        """Test production creation with invalid hospital"""
        production_data = {
            "doctor_id": str(created_doctor.id),
            "hospital_id": str(uuid4()),
            "type": "plantao",
            "date": "2024-01-15",
            "description": "Test"
        }

        response = client.post(
            "/api/v1/productions/",
            json=production_data,
            headers=auth_headers
        )

        assert response.status_code == 404
        assert "Hospital not found" in response.json()["detail"]

    def test_get_all_productions(self, client: TestClient, auth_headers: dict, created_production):
        """Test listing all productions"""
        response = client.get(
            "/api/v1/productions/",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_production_by_id(self, client: TestClient, auth_headers: dict, created_production):
        """Test getting production by ID"""
        response = client.get(
            f"/api/v1/productions/{created_production.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(created_production.id)

    def test_get_productions_by_doctor(self, client: TestClient, auth_headers: dict,
                                       created_doctor, created_production):
        """Test getting productions by doctor"""
        response = client.get(
            f"/api/v1/productions/doctor/{created_doctor.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["doctor_id"] == str(created_doctor.id)

    def test_update_production(self, client: TestClient, auth_headers: dict, created_production):
        """Test updating production"""
        update_data = {
            "type": "consulta",
            "date": "2024-01-16",
            "description": "Updated description"
        }

        response = client.put(
            f"/api/v1/productions/{created_production.id}",
            json=update_data,
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "consulta"
        assert data["description"] == "Updated description"

    def test_delete_production(self, client: TestClient, auth_headers: dict, created_production):
        """Test deleting production"""
        response = client.delete(
            f"/api/v1/productions/{created_production.id}",
            headers=auth_headers
        )

        assert response.status_code == 200


class TestRepasseRoutes:
    """Integration tests for repasse endpoints"""

    def test_create_repasse_success(self, client: TestClient, auth_headers: dict,
                                    created_production):
        """Test successful repasse creation"""
        repasse_data = {
            "production_id": str(created_production.id),
            "valor": 1500.00
        }

        response = client.post(
            "/api/v1/repasses/",
            json=repasse_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()
        assert data["production_id"] == str(created_production.id)
        assert float(data["valor"]) == 1500.00

    def test_create_repasse_invalid_production(self, client: TestClient, auth_headers: dict):
        """Test repasse creation with invalid production"""
        repasse_data = {
            "production_id": str(uuid4()),
            "valor": 1500.00
        }

        response = client.post(
            "/api/v1/repasses/",
            json=repasse_data,
            headers=auth_headers
        )

        assert response.status_code == 404
        assert "Production not found" in response.json()["detail"]

    def test_get_all_repasses(self, client: TestClient, auth_headers: dict, created_production):
        """Test listing all repasses"""
        # Create a repasse first
        client.post(
            "/api/v1/repasses/",
            json={
                "production_id": str(created_production.id),
                "valor": 1500.00
            },
            headers=auth_headers
        )

        response = client.get(
            "/api/v1/repasses/",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_repasses_by_production(self, client: TestClient, auth_headers: dict,
                                        created_production):
        """Test getting repasses by production"""
        # Create a repasse
        create_response = client.post(
            "/api/v1/repasses/",
            json={
                "production_id": str(created_production.id),
                "valor": 1500.00
            },
            headers=auth_headers
        )

        response = client.get(
            f"/api/v1/repasses/production/{created_production.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["production_id"] == str(created_production.id)

    def test_update_repasse(self, client: TestClient, auth_headers: dict, created_production):
        """Test updating repasse"""
        # Create repasse
        create_response = client.post(
            "/api/v1/repasses/",
            json={
                "production_id": str(created_production.id),
                "valor": 1500.00
            },
            headers=auth_headers
        )
        repasse_id = create_response.json()["id"]

        # Update repasse
        update_data = {"valor": 2000.00}
        response = client.put(
            f"/api/v1/repasses/{repasse_id}",
            json=update_data,
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert float(data["valor"]) == 2000.00

    def test_delete_repasse(self, client: TestClient, auth_headers: dict, created_production):
        """Test deleting repasse"""
        # Create repasse
        create_response = client.post(
            "/api/v1/repasses/",
            json={
                "production_id": str(created_production.id),
                "valor": 1500.00
            },
            headers=auth_headers
        )
        repasse_id = create_response.json()["id"]

        # Delete repasse
        response = client.delete(
            f"/api/v1/repasses/{repasse_id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]
