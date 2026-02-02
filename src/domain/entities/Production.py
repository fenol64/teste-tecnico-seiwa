import uuid
from pydantic import BaseModel
from datetime import date


class Production(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    doctor_id: uuid.UUID
    hospital_id: uuid.UUID
    type: str  # "plantao" ou "consulta"
    date: date
    description: str | None = None
    created_at: str
    updated_at: str | None = None

    def __init__(self, **data):
        super().__init__(**data)
