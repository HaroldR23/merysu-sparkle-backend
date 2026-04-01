"""Add contact fields to customers table

Revision ID: b5c2d3e4f6a7
Revises: a3f7e9b2c1d5
Create Date: 2026-04-01 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b5c2d3e4f6a7"
down_revision: Union[str, Sequence[str], None] = "a3f7e9b2c1d5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("customers", sa.Column("email", sa.String(), nullable=True))
    op.add_column("customers", sa.Column("phone_number", sa.String(), nullable=True))
    op.add_column("customers", sa.Column("location", sa.String(), nullable=True))
    op.add_column("customers", sa.Column("city", sa.String(), nullable=True))
    op.add_column("customers", sa.Column("notes", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("customers", "notes")
    op.drop_column("customers", "city")
    op.drop_column("customers", "location")
    op.drop_column("customers", "phone_number")
    op.drop_column("customers", "email")
