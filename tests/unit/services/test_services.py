"""Unit tests for services"""
import pytest
from src.infrastructure.services.password_service import PasswordService
from src.infrastructure.services.jwt_service import JWTService
from uuid import uuid4


class TestPasswordService:
    """Test cases for PasswordService"""

    def test_hash_password(self, password_service: PasswordService):
        """Test password hashing"""
        password = "SecurePassword123"
        hashed = password_service.encrypt_password(password)

        assert hashed is not None
        assert hashed != password
        assert len(hashed) > 0

    def test_verify_password_correct(self, password_service: PasswordService):
        """Test password verification with correct password"""
        password = "SecurePassword123"
        hashed = password_service.encrypt_password(password)

        result = password_service.verify_password(password, hashed)

        assert result is True

    def test_verify_password_incorrect(self, password_service: PasswordService):
        """Test password verification with incorrect password"""
        password = "SecurePassword123"
        wrong_password = "WrongPassword456"
        hashed = password_service.encrypt_password(password)

        result = password_service.verify_password(wrong_password, hashed)

        assert result is False

    def test_hash_password_different_outputs(self, password_service: PasswordService):
        """Test that same password produces different hashes"""
        password = "SecurePassword123"
        hash1 = password_service.encrypt_password(password)
        hash2 = password_service.encrypt_password(password)

        # Hashes should be different due to salt
        assert hash1 != hash2
        # But both should verify correctly
        assert password_service.verify_password(password, hash1)
        assert password_service.verify_password(password, hash2)


class TestJWTService:
    """Test cases for JWTService"""

    def test_create_access_token(self):
        """Test JWT token creation"""
        jwt_service = JWTService()
        user_id = str(uuid4())

        token = jwt_service.create_access_token(data={"sub": user_id})

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_verify_token_valid(self):
        """Test verifying valid JWT token"""
        jwt_service = JWTService()
        user_id = str(uuid4())

        token = jwt_service.create_access_token(data={"sub": user_id})
        decoded = jwt_service.verify_token(token)

        assert decoded is not None
        assert decoded["sub"] == user_id

    def test_verify_token_invalid(self):
        """Test verifying invalid JWT token"""
        jwt_service = JWTService()
        invalid_token = "invalid.token.here"

        try:
            jwt_service.verify_token(invalid_token)
            assert False, "Should have raised ValueError"
        except ValueError:
            assert True

    def test_verify_token_expired(self):
        """Test verifying token with invalid signature"""
        jwt_service = JWTService()

        # Token with invalid signature
        fake_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.invalid"

        try:
            jwt_service.verify_token(fake_token)
            assert False, "Should have raised ValueError"
        except ValueError:
            assert True
