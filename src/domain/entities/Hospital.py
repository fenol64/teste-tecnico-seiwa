import uuid
from pydantic import BaseModel
from datetime import datetime

class Hospital(BaseModel):
    id: uuid.UUID
    name: str
    address: str
    user_id: uuid.UUID
    created_at: str
    updated_at: str | None = None

    def __init__(self, **data):
        super().__init__(**data)
