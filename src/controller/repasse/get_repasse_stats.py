from typing import Optional
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, Query, status
from src.bootstrap.provider import usecase_factory
from src.domain.usecase.repasse.get_repasse_stats import GetRepasseStatsUseCase
from src.dto.repasseDTO import RepasseStatsDTO
from src.infrastructure.auth.dependencies import get_current_user


def get_repasse_stats(
    doctor_id: UUID,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    use_case: GetRepasseStatsUseCase = Depends(usecase_factory("get_repasse_stats_use_case")),
    current_user: dict = Depends(get_current_user)
) -> RepasseStatsDTO:
    return use_case.execute(doctor_id, start_date, end_date)
