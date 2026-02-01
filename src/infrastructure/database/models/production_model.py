from sqlalchemy import Column, String, DateTime, Date, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid
import enum

from src.infrastructure.database.connection import Base


class ProductionType(str, enum.Enum):
    SHIFT = "shift"
    CONSULTATION = "consultation"


class ProductionModel(Base):
    __tablename__ = "productions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False, index=True)
    hospital_id = Column(UUID(as_uuid=True), ForeignKey("hospitals.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(Enum(ProductionType), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Production(id={self.id}, doctor_id={self.doctor_id}, type={self.type}, date={self.date})>"
