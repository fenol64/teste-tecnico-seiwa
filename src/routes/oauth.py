from fastapi import APIRouter, Depends
from src.bootstrap.provider import usecase_factory
from src.controller.oauth.signup import SignUpHandler
from src.domain.usecase.oauth.signup import SignUpUseCase
from src.dto.signup import CreateUserDTO

router = APIRouter()

@router.post('/signup')
async def signup(user: CreateUserDTO, signup_usecase: SignUpUseCase = Depends(usecase_factory('signup'))):
    handler = SignUpHandler(sign_up_usecase=signup_usecase)
    return handler.handle(user)
