from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid
from src.infrastructure.database.connection import Base
from src.domain.enums.repasse_status import RepasseStatus


class RepasseModel(Base):
    __tablename__ = "repasses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    production_id = Column(UUID(as_uuid=True), ForeignKey("productions.id", ondelete="CASCADE"), nullable=False, index=True)
    valor = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    status = Column(SAEnum(RepasseStatus), default=RepasseStatus.PENDING, nullable=False)
