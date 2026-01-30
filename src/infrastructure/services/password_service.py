from passlib.context import CryptContext
from src.domain.usecase.interfaces.IEncrypt_password import IEncryptPassword

class PasswordService(IEncryptPassword):
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def encrypt_password(self, password: str) -> str:
        """Encripta a senha usando bcrypt"""
        # Bcrypt limita senhas a 72 bytes, truncar se necessário
        password_bytes = password.encode('utf-8')[:72]
        password_truncated = password_bytes.decode('utf-8', errors='ignore')
        return self.pwd_context.hash(password_truncated)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica se a senha corresponde ao hash"""
        # Bcrypt limita senhas a 72 bytes, truncar se necessário
        password_bytes = plain_password.encode('utf-8')[:72]
        password_truncated = password_bytes.decode('utf-8', errors='ignore')
        return self.pwd_context.verify(password_truncated, hashed_password)
