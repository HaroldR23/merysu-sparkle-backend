from dataclasses import dataclass
from datetime import date


@dataclass
class EmployeeCreationInput:
    name: str
    entry_date: date
    services_count: int
    phone_number: str
    worked_hours: float
    employee_cost: float
