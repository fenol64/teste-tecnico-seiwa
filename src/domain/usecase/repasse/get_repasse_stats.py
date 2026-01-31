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

        pendente_qtd = 0
        pendente_valor = Decimal(0)
        consolidado_qtd = 0
        consolidado_valor = Decimal(0)

        for repasse in repasses:
            if repasse.status == RepasseStatus.PENDENTE:
                pendente_qtd += 1
                pendente_valor += repasse.valor
            elif repasse.status == RepasseStatus.CONSOLIDADO:
                consolidado_qtd += 1
                consolidado_valor += repasse.valor

        return RepasseStatsDTO(
            doctor_id=doctor_id,
            periodo_inicio=start_date,
            periodo_fim=end_date,
            total_pendente_qtd=pendente_qtd,
            total_pendente_valor=pendente_valor,
            total_consolidado_qtd=consolidado_qtd,
            total_consolidado_valor=consolidado_valor
        )
