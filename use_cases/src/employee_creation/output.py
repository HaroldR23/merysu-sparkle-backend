from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass
class EmployeeCreationOutput:
    id: UUID
    name: str
    entry_date: date
    services_count: int
    phone_number: str
    worked_hours: float
    employee_cost: float
