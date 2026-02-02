from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
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
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Doctor(id={self.id}, name={self.name}, crm={self.crm}, specialty={self.specialty})>"
