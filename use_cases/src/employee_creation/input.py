from dataclasses import dataclass


@dataclass
class EmployeeCreationInput:
    name: str
    services_count: int
    phone_number: str
    worked_hours: float
    employee_cost: float
