from dataclasses import dataclass
from datetime import date, datetime, time
from enum import Enum
from uuid import UUID


class ServiceType(str, Enum):
    residential_cleaning = "residential_cleaning"
    commercial_cleaning = "commercial_cleaning"
    deep_cleaning = "deep_cleaning"
    move_in_out = "move_in_out"
    post_construction = "post_construction"


@dataclass
class Service:
    date: date
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
    employee_id: UUID | None = None
    internal_notes: str | None = None
    id: UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
