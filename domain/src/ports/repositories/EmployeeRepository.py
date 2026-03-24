from abc import ABC, abstractmethod
from uuid import UUID

from domain.src.entities.employee import Employee, EmployeeSummary


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
