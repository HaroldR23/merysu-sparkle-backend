from dataclasses import dataclass

from domain.src.entities.customer import CustomerStatus, CustomerType


@dataclass
class CustomerListInput:
    status: CustomerStatus | None = None
    type: CustomerType | None = None
    search: str | None = None
    page: int = 1
    page_size: int = 20
