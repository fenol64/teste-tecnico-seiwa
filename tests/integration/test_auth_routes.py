"""Integration tests for Authentication routes"""
import pytest
from fastapi.testclient import TestClient


class TestAuthRoutes:
    """Integration tests for authentication endpoints"""

    def test_signup_success(self, client: TestClient):
        """Test successful user registration"""
        user_data = {
            "name": "New User",
            "email": "newuser@example.com",
            "password": "SecurePass@123"
        }

        response = client.post(
            "/api/v1/signup",
            json=user_data
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert "message" in data

    def test_signup_duplicate_email(self, client: TestClient, created_user):
        """Test signup with duplicate email"""
        user_data = {
            "name": "Another User",
            "email": "test@example.com",  # Same as created_user
            "password": "SecurePass@123"
        }

        response = client.post(
            "/api/v1/signup",
            json=user_data
        )

        assert response.status_code == 400
        assert "email already exists" in response.json()["detail"].lower()

    def test_signup_invalid_email(self, client: TestClient):
        """Test signup with invalid email format"""
        user_data = {
            "name": "Test User",
            "email": "invalid-email",
            "password": "SecurePass@123"
        }

        response = client.post(
            "/api/v1/signup",
            json=user_data
        )

        assert response.status_code == 422  # Validation error

    def test_signin_success(self, client: TestClient, created_user):
        """Test successful user login"""
        credentials = {
            "email": "test@example.com",
            "password": "Test@1234"
        }

        response = client.post(
            "/api/v1/signin",
            json=credentials
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == credentials["email"]

    def test_signin_wrong_password(self, client: TestClient, created_user):
        """Test login with wrong password"""
        credentials = {
            "email": "test@example.com",
            "password": "WrongPassword123"
        }

        response = client.post(
            "/api/v1/signin",
            json=credentials
        )

        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    def test_signin_nonexistent_user(self, client: TestClient):
        """Test login with non-existent user"""
        credentials = {
            "email": "nonexistent@example.com",
            "password": "Password123"
        }

        response = client.post(
            "/api/v1/signin",
            json=credentials
        )

        assert response.status_code == 401

    def test_protected_route_without_token(self, client: TestClient):
        """Test accessing protected route without token"""
        response = client.get("/api/v1/doctors/")

        # May return 401 or 403 depending on implementation
        assert response.status_code in [401, 403]

    def test_protected_route_with_valid_token(self, client: TestClient, auth_headers: dict):
        """Test accessing protected route with valid token"""
        response = client.get(
            "/api/v1/doctors/",
            headers=auth_headers
        )

        assert response.status_code == 200


class TestHealthCheck:
    """Integration tests for health check endpoint"""

    def test_health_check(self, client: TestClient):
        """Test health check endpoint"""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
