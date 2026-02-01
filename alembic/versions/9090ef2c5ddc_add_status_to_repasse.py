"""add status to repasse

Revision ID: 9090ef2c5ddc
Revises: 3940d94fd0b7
Create Date: 2026-01-31 02:58:30.559807

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9090ef2c5ddc'
down_revision: Union[str, None] = '3940d94fd0b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Criar o tipo ENUM primeiro
    repasse_status_enum = postgresql.ENUM('PENDENTE', 'CONSOLIDADO', name='repassestatus', create_type=True)
    repasse_status_enum.create(op.get_bind(), checkfirst=True)

    # Adicionar a coluna usando o ENUM criado
    op.add_column('repasses', sa.Column('status', sa.Enum('PENDENTE', 'CONSOLIDADO', name='repassestatus'), nullable=False, server_default='PENDENTE'))


def downgrade() -> None:
    # Remover a coluna
    op.drop_column('repasses', 'status')

    # Remover o tipo ENUM
    repasse_status_enum = postgresql.ENUM('PENDENTE', 'CONSOLIDADO', name='repassestatus')
    repasse_status_enum.drop(op.get_bind(), checkfirst=True)