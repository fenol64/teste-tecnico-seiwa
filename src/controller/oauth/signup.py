from fastapi import HTTPException
from src.dto.createUserDTO import CreateUserDTO
from src.domain.usecase.oauth.signup import SignUpUseCase


class SignUpHandler:
    def __init__ (self, sign_up_usecase: SignUpUseCase):
        self.sign_up_usecase = sign_up_usecase

    def handle(self, user_data: CreateUserDTO):
        """Handler para cadastro de novos usuários"""
        try:
            self.sign_up_usecase.execute(user_data)
            return {
                "message": "Usuário cadastrado com sucesso!",
                "email": user_data.email
            }
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Erro interno ao cadastrar usuário")