import uuid
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class SignInDTO(BaseModel):
    """DTO for user login"""
    email: EmailStr = Field(..., description="User email (must be valid)")
    password: str = Field(..., min_length=6, max_length=100, description="User password (min 6 chars)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "secretpassword"
            }
        }
    )
