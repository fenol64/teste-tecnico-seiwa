from fastapi import APIRouter, Depends, status
from src.bootstrap.provider import usecase_factory
from src.controller.oauth.signup import SignUpHandler
from src.controller.oauth.signin import SignInHandler
from src.domain.usecase.oauth.signup import SignUpUseCase
from src.domain.usecase.oauth.signin import SignInUseCase
from src.dto.createUserDTO import CreateUserDTO
from src.dto.signinDTO import SignInDTO
from src.dto.responses import SignUpResponse, SignInResponse, ErrorResponse

router = APIRouter()

@router.post(
    '/signup',
    summary="User Registration",
    description="Creates a new user in the system with email and password",
    response_model=SignUpResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "User registered successfully",
            "model": SignUpResponse
        },
        400: {
            "description": "Invalid data or email already registered",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "User with this email already exists."}
                }
            }
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "email"],
                                "msg": "value is not a valid email address",
                                "type": "value_error.email"
                            }
                        ]
                    }
                }
            }
        },
        500: {
            "description": "Internal Server Error",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "Internal error while registering user"}
                }
            }
        }
    }
)
async def signup(
    user: CreateUserDTO,
    signup_usecase: SignUpUseCase = Depends(usecase_factory('signup_usecase'))
):
    handler = SignUpHandler(sign_up_usecase=signup_usecase)
    return handler.handle(user)


@router.post(
    '/signin',
    summary="User Login",
    description="Authenticates an existing user in the system",
    response_model=SignInResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Login successful",
            "model": SignInResponse
        },
        400: {
            "description": "Invalid credentials",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid email or password"}
                }
            }
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "email"],
                                "msg": "value is not a valid email address",
                                "type": "value_error.email"
                            }
                        ]
                    }
                }
            }
        },
        500: {
            "description": "Internal Server Error",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "Internal error during login"}
                }
            }
        }
    }
)
async def signin(
    user: SignInDTO,
    signin_usecase: SignInUseCase = Depends(usecase_factory('signin_usecase'))
):
    handler = SignInHandler(sign_in_usecase=signin_usecase)
    return handler.handle(user)
