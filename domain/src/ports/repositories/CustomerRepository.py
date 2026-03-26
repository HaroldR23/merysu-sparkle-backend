from abc import ABC, abstractmethod
from uuid import UUID

from domain.src.entities.customer import Customer, CustomerStatus, CustomerSummary, CustomerType


class CustomerRepository(ABC):
    @abstractmethod
    def create(self, customer: Customer) -> Customer:
        """Persist a new customer and return it with the assigned id."""
        pass

    @abstractmethod
    def get_by_id(self, id: UUID) -> Customer | None:
        """Return the customer with the given id, or None if not found."""
        pass

    @abstractmethod
    def get_all_with_summary(
        self,
        status: CustomerStatus | None,
        type: CustomerType | None,
        search: str | None,
        offset: int,
        limit: int,
    ) -> tuple[list[Customer], CustomerSummary]:
        """Return a filtered, paginated list of customers alongside global aggregated metrics."""
        pass
