from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.src.entities.customer import CustomerStatus, CustomerType


@dataclass
class CustomerUpdateInput:
    id: UUID
    name: str | None = None
    type: CustomerType | None = None
    status: CustomerStatus | None = None
    services_count: int | None = None
    total_billed: float | None = None
    last_service_date: datetime | None = None
    email: str | None = None
    phone_number: str | None = None
    location: str | None = None
    city: str | None = None
    notes: str | None = None
