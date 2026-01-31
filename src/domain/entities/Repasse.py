from datetime import datetime
from decimal import Decimal
from uuid import UUID


class Repasse:
    def __init__(
        self,
        id: UUID,
        production_id: UUID,
        valor: Decimal,
        created_at: datetime,
        updated_at: datetime
    ):
        self.id = id
        self.production_id = production_id
        self.valor = valor
        self.created_at = created_at
        self.updated_at = updated_at
