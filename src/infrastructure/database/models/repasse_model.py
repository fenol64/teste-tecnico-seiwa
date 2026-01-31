from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from src.infrastructure.database.connection import Base


class RepasseModel(Base):
    __tablename__ = "repasses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    production_id = Column(UUID(as_uuid=True), ForeignKey("productions.id", ondelete="CASCADE"), nullable=False, index=True)
    valor = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
