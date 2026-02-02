from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import Optional
from src.domain.enums.repasse_status import RepasseStatus


class Repasse:
    def __init__(
        self,
        id: UUID,
        user_id: UUID,
        production_id: UUID,
        amount: Decimal,
        created_at: datetime,
        updated_at: datetime,
        status: RepasseStatus = RepasseStatus.PENDING
    ):
        self.id = id
        self.user_id = user_id
        self.production_id = production_id
        self.amount = amount
        self.created_at = created_at
        self.updated_at = updated_at
        self.status = status
