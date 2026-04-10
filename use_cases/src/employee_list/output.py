from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass
class EmployeeSummaryOutput:
    total_employees: int
    total_hours: float
    total_cost: float
    total_services: int


@dataclass
class EmployeeListItemOutput:
    id: UUID
    name: str
    entry_date: date
    phone_number: str
    worked_hours: float
    employee_cost: float
    services_count: int
    productivity: float


@dataclass
class EmployeeListOutput:
    summary: EmployeeSummaryOutput
    employees: list[EmployeeListItemOutput]
