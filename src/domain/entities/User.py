import uuid
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    password: str
    created_at: str
    updated_at: str | None = None

    def __init__(self, **data):
        # VERIFY EMAIL AND PASSWORD FORMATS IF NEEDED
        super().__init__(**data)