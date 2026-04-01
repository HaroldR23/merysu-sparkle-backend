from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.src.entities.customer import CustomerStatus, CustomerType


@dataclass
class CustomerSummaryOutput:
    total_clients: int
    total_billing: float
    total_services: int
    average_billing_per_client: float


@dataclass
class CustomerListItemOutput:
    id: UUID
    name: str
    type: CustomerType
    services_count: int
    total_billed: float
    status: CustomerStatus
    last_service_date: datetime | None
    email: str | None = None
    phone_number: str | None = None
    location: str | None = None
    city: str | None = None
    notes: str | None = None


@dataclass
class CustomerListOutput:
    summary: CustomerSummaryOutput
    customers: list[CustomerListItemOutput]
