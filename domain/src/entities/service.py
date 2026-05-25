from dataclasses import dataclass, field
from datetime import date, datetime, time
from enum import Enum
from uuid import UUID


class ServiceType(str, Enum):
    residential_cleaning = "residential_cleaning"
    commercial_cleaning = "commercial_cleaning"
    deep_cleaning = "deep_cleaning"
    move_in_out = "move_in_out"
    post_construction = "post_construction"


class ServiceStatus(str, Enum):
    completed = "completed"
    pending = "pending"


@dataclass
class Service:
    date: datetime
    start_time: time
    end_time: time
    customer_id: UUID
    address: str
    service_type: ServiceType
    distance_km: float
    worked_hours: float
    hourly_rate: float
    total_cost: float
    charged_price: float
    status: ServiceStatus
    employee_ids: list[UUID] = field(default_factory=list)
    internal_notes: str | None = None
    id: UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class ServiceListItem:
    id: UUID
    date: datetime
    start_time: time
    end_time: time
    customer_id: UUID
    customer_name: str
    address: str
    service_type: ServiceType
    distance_km: float
    hourly_rate: float
    employee_names: list[str]
    worked_hours: float
    charged_price: float
    total_cost: float
    margin: float
    status: ServiceStatus
    internal_notes: str | None = None
