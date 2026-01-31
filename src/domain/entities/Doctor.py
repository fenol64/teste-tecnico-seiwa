import uuid
from pydantic import BaseModel
from datetime import datetime

class Doctor(BaseModel):
    id: uuid.UUID
    name: str
    crm: str
    specialty: str
    phone: str | None = None
    email: str
    created_at: str
    updated_at: str | None = None

    def __init__(self, **data):
        super().__init__(**data)
