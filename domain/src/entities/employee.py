from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from uuid import UUID


class EmployeeStatus(str, Enum):
    active = "active"
    inactive = "inactive"


@dataclass
class Employee:
    name: str
    entry_date: date
    services_count: int
    phone_number: str
    worked_hours: float
    employee_cost: float
    id: UUID | None = None
    notes: str | None = None
    status: EmployeeStatus = field(default=EmployeeStatus.active)


@dataclass
class EmployeeSummary:
    total_employees: int
    total_hours: float
    total_cost: float
    total_services: int
