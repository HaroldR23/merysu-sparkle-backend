from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass
class Employee:
    name: str
    entry_date: date
    services_count: int
    phone_number: str
    worked_hours: float
    employee_cost: float
    id: UUID | None = None


@dataclass
class EmployeeSummary:
    total_employees: int
    total_hours: float
    total_cost: float
    total_services: int
