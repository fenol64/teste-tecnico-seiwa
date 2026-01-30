import uuid
from pydantic import BaseModel

class CreateUserDTO(BaseModel):
    name: str
    email: str | None = None
    password: str