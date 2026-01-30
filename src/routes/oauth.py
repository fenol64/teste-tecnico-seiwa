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
    summary="Cadastro de Usuário",
    description="Cria um novo usuário no sistema com email e senha",
    response_model=SignUpResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Usuário cadastrado com sucesso",
            "model": SignUpResponse
        },
        400: {
            "description": "Dados inválidos ou email já cadastrado",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "User with this email already exists."}
                }
            }
        },
        422: {
            "description": "Erro de validação",
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
            "description": "Erro interno do servidor",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "Erro interno ao cadastrar usuário"}
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
    summary="Login de Usuário",
    description="Autentica um usuário existente no sistema",
    response_model=SignInResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Login realizado com sucesso",
            "model": SignInResponse
        },
        400: {
            "description": "Credenciais inválidas",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid email or password"}
                }
            }
        },
        422: {
            "description": "Erro de validação",
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
            "description": "Erro interno do servidor",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "Erro interno ao fazer login"}
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
