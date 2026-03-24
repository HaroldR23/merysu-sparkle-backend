from abc import ABC, abstractmethod
from uuid import UUID

from domain.src.entities.employee import Employee


class EmployeeRepository(ABC):
    @abstractmethod
    def create(self, employee: Employee) -> Employee:
        """Persist a new employee and return it with the assigned id."""
        pass

    @abstractmethod
    def get_by_id(self, id: UUID) -> Employee | None:
        """Return the employee with the given id, or None if not found."""
        pass
