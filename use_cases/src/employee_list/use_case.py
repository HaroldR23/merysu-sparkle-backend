from typing import cast
from uuid import UUID

from domain.src.ports.repositories.EmployeeRepository import EmployeeRepository
from use_cases.src.employee_list.output import (
    EmployeeListItemOutput,
    EmployeeListOutput,
    EmployeeSummaryOutput,
)


class EmployeeListUseCase:
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    def __call__(self) -> EmployeeListOutput:
        employees, summary = self.employee_repository.get_all_with_summary()

        return EmployeeListOutput(
            summary=EmployeeSummaryOutput(
                total_employees=summary.total_employees,
                total_hours=summary.total_hours,
                total_cost=summary.total_cost,
                total_services=summary.total_services,
            ),
            employees=[
                EmployeeListItemOutput(
                    id=cast(UUID, e.id),
                    name=e.name,
                    worked_hours=e.worked_hours,
                    employee_cost=e.employee_cost,
                    services_count=e.services_count,
                )
                for e in employees
            ],
        )
