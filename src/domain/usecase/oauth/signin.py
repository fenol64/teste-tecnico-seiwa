from src.domain.entities.User import User
from src.domain.usecase.interfaces.IEncrypt_password import IEncryptPassword
from src.domain.usecase.interfaces.IGetUserByEmail import IGetUserByEmail
from src.domain.usecase.interfaces.ITokenService import ITokenService
from src.dto.signinDTO import SignInDTO


class SignInUseCase:
    def __init__(
        self,
        get_user_by_email_port: IGetUserByEmail,
        encrypt_password_port: IEncryptPassword,
        token_service_port: ITokenService
    ):
        self.get_user_by_email_port = get_user_by_email_port
        self.encrypt_password_port = encrypt_password_port
        self.token_service_port = token_service_port

    def execute(self, user_data: SignInDTO) -> dict:
        # Buscar usuário pelo email
        user = self.get_user_by_email_port.get_user_by_email(user_data.email)

        if not user:
            raise ValueError("Invalid email or password")

        # Verificar senha
        is_valid = self.encrypt_password_port.verify_password(
            user_data.password,
            user.password
        )

        if not is_valid:
            raise ValueError("Invalid email or password")

        # Gerar token JWT
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "name": user.name
        }
        access_token = self.token_service_port.create_access_token(data=token_data)

        # Retornar dados do usuário com token
        return {
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id),
                "name": user.name,
                "email": user.email
            }
        }
