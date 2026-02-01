"""update_enums

Revision ID: fdb9687fbf8c
Revises: 02f2d5d04257
Create Date: 2026-02-01 20:17:40.253078

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fdb9687fbf8c'
down_revision: Union[str, None] = '02f2d5d04257'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### Updated Enums ###
    
    # 1. Update Production Types
    op.execute("ALTER TYPE productiontype RENAME TO productiontype_old")
    op.execute("CREATE TYPE productiontype AS ENUM('shift', 'consultation')")
    op.execute("""
        ALTER TABLE productions 
        ALTER COLUMN type TYPE productiontype 
        USING (
            CASE lower(type::text) 
                WHEN 'plantao' THEN 'shift'::productiontype
                WHEN 'consulta' THEN 'consultation'::productiontype
                WHEN 'shift' THEN 'shift'::productiontype
                WHEN 'consultation' THEN 'consultation'::productiontype
                -- If we encounter something unexpected, default to shift or try to cast
                ELSE 'shift'::productiontype 
            END
        )
    """)
    op.execute("DROP TYPE productiontype_old")

    # 2. Update Repasse Status
    op.execute("ALTER TYPE repassestatus RENAME TO repassestatus_old")
    op.execute("CREATE TYPE repassestatus AS ENUM('pending', 'consolidated')")
    op.execute("""
        ALTER TABLE repasses 
        ALTER COLUMN status TYPE repassestatus 
        USING (
            CASE lower(status::text) 
                WHEN 'pendente' THEN 'pending'::repassestatus
                WHEN 'consolidado' THEN 'consolidated'::repassestatus
                WHEN 'pending' THEN 'pending'::repassestatus
                WHEN 'consolidated' THEN 'consolidated'::repassestatus
                ELSE 'pending'::repassestatus
            END
        )
    """)
    op.execute("DROP TYPE repassestatus_old")


def downgrade() -> None:
    # Downgrade logic (simplified, assuming we want to go back to previous state)
    # This might be lossy if we have new 'shift' values that don't map back perfectly if strict
    pass
