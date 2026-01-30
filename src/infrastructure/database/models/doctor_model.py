from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from src.infrastructure.database.connection import Base

class DoctorModel(Base):
    __tablename__ = "doctors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    crm = Column(String(20), unique=True, nullable=False, index=True)
    specialty = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now().isoformat(), nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.now().isoformat())

    def __repr__(self):
        return f"<Doctor(id={self.id}, name={self.name}, crm={self.crm}, specialty={self.specialty})>"
