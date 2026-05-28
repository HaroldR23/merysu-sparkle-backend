from dataclasses import dataclass
from datetime import date
from uuid import UUID

from domain.src.entities.employee import EmployeeStatus


@dataclass
class EmployeeUpdateInput:
    id: UUID
    name: str | None = None
    entry_date: date | None = None
    phone_number: str | None = None
    services_count: int | None = None
    worked_hours: float | None = None
    employee_cost: float | None = None
    notes: str | None = None
    status: EmployeeStatus | None = None
