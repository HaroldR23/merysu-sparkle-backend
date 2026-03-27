"""update_services_table_many_to_many_employees_and_status

Revision ID: a3f7e9b2c1d5
Revises: 42479565102b
Create Date: 2026-03-27 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "a3f7e9b2c1d5"
down_revision: Union[str, Sequence[str], None] = "42479565102b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create service_employees association table
    op.create_table(
        "service_employees",
        sa.Column("service_id", sa.Uuid(), nullable=False),
        sa.Column("employee_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"]),
        sa.ForeignKeyConstraint(["service_id"], ["services.id"]),
        sa.PrimaryKeyConstraint("service_id", "employee_id"),
    )

    # 2. Migrate existing single employee_id rows into the new table
    op.execute(
        "INSERT INTO service_employees (service_id, employee_id) "
        "SELECT id, employee_id FROM services WHERE employee_id IS NOT NULL"
    )

    # 3. Add status column + drop employee_id column
    with op.batch_alter_table("services") as bop:
        bop.add_column(
            sa.Column(
                "status",
                sa.String(),
                nullable=False,
                server_default="completed",
            )
        )
        bop.drop_column("employee_id")


def downgrade() -> None:
    # 1. Re-add employee_id, populate from service_employees (first employee only)
    with op.batch_alter_table("services") as bop:
        bop.add_column(sa.Column("employee_id", sa.Uuid(), nullable=True))
        bop.drop_column("status")

    op.execute(
        "UPDATE services SET employee_id = ("
        "  SELECT employee_id FROM service_employees"
        "  WHERE service_employees.service_id = services.id LIMIT 1"
        ")"
    )

    # 2. Drop association table
    op.drop_table("service_employees")
