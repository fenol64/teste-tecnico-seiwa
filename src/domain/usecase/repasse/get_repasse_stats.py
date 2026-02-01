from typing import Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from src.domain.usecase.interfaces.repasse_repository_interface import IRepasseRepository
from src.dto.repasseDTO import RepasseStatsDTO
from src.domain.enums.repasse_status import RepasseStatus

class GetRepasseStatsUseCase:
    def __init__(self, repasse_repository: IRepasseRepository):
        self.repasse_repository = repasse_repository

    def execute(
        self,
        doctor_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> RepasseStatsDTO:
        repasses = self.repasse_repository.get_by_doctor_and_date_range(doctor_id, start_date, end_date)

        pending_count = 0
        pending_value = Decimal(0)
        consolidated_count = 0
        consolidated_value = Decimal(0)

        for repasse in repasses:
            if repasse.status == RepasseStatus.PENDING:
                pending_count += 1
                pending_value += repasse.amount
            elif repasse.status == RepasseStatus.CONSOLIDATED:
                consolidated_count += 1
                consolidated_value += repasse.amount

        return RepasseStatsDTO(
            doctor_id=doctor_id,
            period_start=start_date,
            period_end=end_date,
            total_pending_count=pending_count,
            total_pending_value=pending_value,
            total_consolidated_count=consolidated_count,
            total_consolidated_value=consolidated_value
        )
