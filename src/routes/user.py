from fastapi import APIRouter, Depends, status
from typing import Dict, Any

from src.infrastructure.auth.dependencies import get_current_user
from src.dto.responses import UserData

router = APIRouter()

@router.get(
    "/me",
    summary="Get Current User Data",
    description="Returns the authenticated user data (protected route)",
    response_model=UserData,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "User data returned successfully",
            "model": UserData
        },
        401: {
            "description": "Invalid or missing token",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid authentication credentials"}
                }
            }
        }
    }
)
async def get_me(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Protected route that returns the authenticated user's data.

    Requires a valid JWT token in the Authorization header: Bearer <token>

    The token is obtained after successful login at /api/v1/signin
    """
    return {
        "id": current_user.get("sub"),
        "name": current_user.get("name"),
        "email": current_user.get("email")
    }
