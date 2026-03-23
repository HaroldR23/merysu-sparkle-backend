from abc import ABC, abstractmethod

from domain.src.entities.employee import Employee


class EmployeeRepositoryService(ABC):
    @abstractmethod
    def create(self, employee: Employee) -> Employee:
        """Persist a new employee and return it with the assigned id."""
        pass
