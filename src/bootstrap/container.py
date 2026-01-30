from src.domain.usecase.oauth.signup import SignUpUseCase
from src.domain.usecase.oauth.signin import SignInUseCase
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.database.connection import SessionLocal
from src.infrastructure.services.password_service import PasswordService
from src.infrastructure.services.jwt_service import JWTService
from sqlalchemy.orm import Session

class Container:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db=self.db)
        self.password_service = PasswordService()
        self.token_service = JWTService()

        self.signup_usecase = SignUpUseCase(
            get_user_by_email_port=self.user_repository,
            encrypt_password_port=self.password_service,
            save_user_port=self.user_repository
        )

        self.signin_usecase = SignInUseCase(
            get_user_by_email_port=self.user_repository,
            encrypt_password_port=self.password_service,
            token_service_port=self.token_service
        )


