from abc import ABC, abstractmethod
from uuid import UUID

from domain.src.entities.customer import Customer


class CustomerRepository(ABC):
    @abstractmethod
    def create(self, customer: Customer) -> Customer:
        """Persist a new customer and return it with the assigned id."""
        pass

    @abstractmethod
    def get_by_id(self, id: UUID) -> Customer | None:
        """Return the customer with the given id, or None if not found."""
        pass
