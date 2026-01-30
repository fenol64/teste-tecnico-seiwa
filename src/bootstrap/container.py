from src.domain.usecase.oauth.signup import SignUpUseCase
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.database.connection import SessionLocal
from src.infrastructure.services.password_service import PasswordService
from sqlalchemy.orm import Session

class Container:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db=self.db)
        self.password_service = PasswordService()

        self.signup_usecase = SignUpUseCase(
            get_user_by_email_port=self.user_repository,
            encrypt_password_port=self.password_service,
            save_user_port=self.user_repository
        )


