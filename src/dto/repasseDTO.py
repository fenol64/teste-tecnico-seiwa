from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from uuid import UUID
from datetime import datetime
from typing import Optional
from src.domain.enums.repasse_status import RepasseStatus


class CreateRepasseDTO(BaseModel):
    production_id: UUID = Field(..., description="Production ID")
    amount: Decimal = Field(..., gt=0, description="Payment amount")
    status: Optional[RepasseStatus] = Field(default=RepasseStatus.PENDING, description="Payment status")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "production_id": "123e4567-e89b-12d3-a456-426614174000",
                "amount": 1500.00,
                "status": "pending"
            }
        }
    )


class UpdateRepasseDTO(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0, description="Payment amount")
    status: Optional[RepasseStatus] = Field(None, description="Payment status")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "amount": 1800.00,
                "status": "consolidated"
            }
        }
    )


class RepasseResponseDTO(BaseModel):
    id: UUID
    production_id: UUID
    amount: Decimal
    status: RepasseStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "production_id": "123e4567-e89b-12d3-a456-426614174001",
                "amount": 1500.00,
                "status": "pending",
                "created_at": "2024-01-01T10:00:00",
                "updated_at": "2024-01-01T10:00:00"
            }
        }
    )


class RepasseStatsDTO(BaseModel):
    doctor_id: UUID
    period_start: Optional[datetime]
    period_end: Optional[datetime]
    total_pending_count: int
    total_pending_value: Decimal
    total_consolidated_count: int
    total_consolidated_value: Decimal
