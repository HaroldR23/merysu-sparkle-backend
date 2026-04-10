"""Add entry_date to employees table

Revision ID: c1d2e3f4a5b6
Revises: b5c2d3e4f6a7
Create Date: 2026-04-09 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c1d2e3f4a5b6"
down_revision: Union[str, Sequence[str], None] = "b5c2d3e4f6a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "employees",
        sa.Column(
            "entry_date",
            sa.Date(),
            nullable=False,
            server_default=sa.func.current_date(),
        ),
    )


def downgrade() -> None:
    op.drop_column("employees", "entry_date")
