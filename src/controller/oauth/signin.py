from fastapi import HTTPException
from src.dto.signinDTO import SignInDTO
from src.domain.usecase.oauth.signin import SignInUseCase


class SignInHandler:
    def __init__ (self, sign_in_usecase: SignInUseCase):
        self.sign_in_usecase = sign_in_usecase

    def handle(self, user_data: SignInDTO):
        """Handler para login de usuários"""
        try:
            return self.sign_in_usecase.execute(user_data)
        except ValueError as e:
            # ValueError para credenciais inválidas deve retornar 401
            raise HTTPException(status_code=401, detail=str(e))
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Erro interno ao realizar login")