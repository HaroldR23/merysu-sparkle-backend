from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class CustomerType(str, Enum):
    commercial = "commercial"
    residential = "residential"


class CustomerStatus(str, Enum):
    active = "active"
    inactive = "inactive"


@dataclass
class Customer:
    name: str
    type: CustomerType
    services_count: int
    total_billed: float
    status: CustomerStatus
    last_service_date: datetime | None = None
    id: UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
