from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from src.infrastructure.database.connection import Base

class DoctorHospitalModel(Base):
    __tablename__ = "doctor_hospital"

    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctors.id", ondelete="CASCADE"), primary_key=True)
    hospital_id = Column(UUID(as_uuid=True), ForeignKey("hospitals.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<DoctorHospital(doctor_id={self.doctor_id}, hospital_id={self.hospital_id})>"
