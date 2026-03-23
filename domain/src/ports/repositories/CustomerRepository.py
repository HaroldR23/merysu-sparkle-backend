from abc import ABC, abstractmethod

from domain.src.entities.customer import Customer


class CustomerRepository(ABC):
    @abstractmethod
    def create(self, customer: Customer) -> Customer:
        """Persist a new customer and return it with the assigned id."""
        pass
