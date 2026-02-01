import uuid
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class CreateUserDTO(BaseModel):
    """DTO for creating a new user"""
    name: str = Field(..., min_length=3, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email (must be valid)")
    password: str = Field(..., min_length=6, max_length=100, description="User's password (min 6 chars)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "password": "secretpassword"
            }
        }
    )