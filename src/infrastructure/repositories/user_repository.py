from sqlalchemy.orm import Session
from typing import Optional

from src.domain.usecase.interfaces.IGetUserByEmail import IGetUserByEmail
from src.domain.usecase.interfaces.ISaveUser import ISaveUser
from src.domain.entities.User import User
from src.infrastructure.database.models.user_model import UserModel


class UserRepository(IGetUserByEmail, ISaveUser):
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Busca um usuário pelo email no banco de dados"""
        user_model = self.db.query(UserModel).filter(UserModel.email == email).first()

        if not user_model:
            return None

        # Converte o modelo SQLAlchemy para a entidade de domínio
        return User(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            password=user_model.password,
            created_at=user_model.created_at.isoformat(),
            updated_at=user_model.updated_at.isoformat() if user_model.updated_at else None
        )

    def save_user(self, user: User) -> None:
        """Salva um novo usuário no banco de dados"""
        user_model = UserModel(
            id=user.id,
            name=user.name,
            email=user.email,
            password=user.password
        )

        self.db.add(user_model)
        self.db.commit()
        self.db.refresh(user_model)
