from src.domain.entities.User import User
from src.domain.usecase.interfaces.IEncrypt_password import IEncryptPassword
from src.domain.usecase.interfaces.IGetUserByEmail import IGetUserByEmail
from src.domain.usecase.interfaces.ISaveUser import ISaveUser
from src.dto.createUserDTO import CreateUserDTO
import uuid
from datetime import datetime

class SignUpUseCase:
    def __init__(self, get_user_by_email_port: IGetUserByEmail, encrypt_password_port: IEncryptPassword, save_user_port: ISaveUser):
        self.get_user_by_email_port = get_user_by_email_port
        self.encrypt_password_port = encrypt_password_port
        self.save_user_port = save_user_port

    def execute(self, user_data: CreateUserDTO) -> None:
        existing_user = self.get_user_by_email_port.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError("User with this email already exists.")
        hashed_password = self.encrypt_password_port.encrypt_password(user_data.password)

        userEntity = User(
            id=uuid.uuid4(),
            name=user_data.name,
            email=user_data.email,
            password=hashed_password,
            created_at=datetime.now().isoformat(),
        )

        self.save_user_port.save_user(userEntity)