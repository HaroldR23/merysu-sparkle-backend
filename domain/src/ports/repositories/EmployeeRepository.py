from abc import ABC, abstractmethod
from uuid import UUID

from domain.src.entities.employee import Employee, EmployeeSummary, EmployeeStatus


class EmployeeRepository(ABC):
    @abstractmethod
    def create(self, employee: Employee) -> Employee:
        """Persist a new employee and return it with the assigned id."""
        pass

    @abstractmethod
    def get_by_id(self, id: UUID) -> Employee | None:
        """Return the employee with the given id, or None if not found."""
        pass

    @abstractmethod
    def get_all_with_summary(self) -> tuple[list[Employee], EmployeeSummary]:
        """Return all employees alongside aggregated metrics."""
        pass

    @abstractmethod
    def update_stats(
        self,
        id: UUID,
        services_count_delta: int,
        worked_hours_delta: float,
        employee_cost_delta: float,
    ) -> None:
        """Increment services_count, worked_hours, and employee_cost for the given employee."""
        pass

    @abstractmethod
    def update(self, employee: Employee) -> Employee:
        """Persist updated employee fields and return the refreshed entity."""
        pass
