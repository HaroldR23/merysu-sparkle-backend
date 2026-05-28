from dataclasses import dataclass
from datetime import date
from uuid import UUID

from domain.src.entities.employee import EmployeeStatus


@dataclass
class EmployeeUpdateOutput:
    id: UUID
    name: str
    entry_date: date
    phone_number: str
    services_count: int
    worked_hours: float
    employee_cost: float
    status: EmployeeStatus
    notes: str | None = None
