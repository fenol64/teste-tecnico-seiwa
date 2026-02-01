from pydantic import BaseModel, Field, ConfigDict


class SuccessResponse(BaseModel):
    """Standard success response"""
    message: str = Field(..., description="Success message")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Operation performed successfully"
            }
        }
    )


class SignUpResponse(BaseModel):
    """User registration response"""
    message: str = Field(..., description="Confirmation message")
    email: str = Field(..., description="Registered user email")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "User registered successfully!",
                "email": "user@example.com"
            }
        }
    )


class ErrorResponse(BaseModel):
    """Standard error response"""
    detail: str = Field(..., description="Error details")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Error processing request"
            }
        }
    )


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Application status")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "ok"
            }
        }
    )


class UserData(BaseModel):
    """User data"""
    id: str = Field(..., description="User unique ID")
    name: str = Field(..., description="User name")
    email: str = Field(..., description="User email")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "John Doe",
                "email": "john.doe@example.com"
            }
        }
    )


class SignInResponse(BaseModel):
    """User login response"""
    message: str = Field(..., description="Confirmation message")
    access_token: str = Field(..., description="JWT Access Token")
    token_type: str = Field(default="bearer", description="Token type")
    user: UserData = Field(..., description="Authenticated user data")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Login successful",
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "John Doe",
                    "email": "john.doe@example.com"
                }
            }
        }
    )


class DeleteResponseDTO(BaseModel):
    """Standard deletion response"""
    message: str = Field(..., description="Deletion confirmation message")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Record deleted successfully"
            }
        }
    )
