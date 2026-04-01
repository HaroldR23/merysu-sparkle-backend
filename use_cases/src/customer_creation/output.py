from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.src.entities.customer import CustomerStatus, CustomerType


@dataclass
class CustomerCreationOutput:
    id: UUID
    name: str
    type: CustomerType
    services_count: int
    total_billed: float
    status: CustomerStatus
    created_at: datetime
    updated_at: datetime
    last_service_date: datetime | None = None
    email: str | None = None
    phone_number: str | None = None
    location: str | None = None
    city: str | None = None
    notes: str | None = None
