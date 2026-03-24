from dataclasses import dataclass
from datetime import date, datetime, time
from uuid import UUID

from domain.src.entities.service import ServiceType


@dataclass
class ServiceCreationOutput:
    id: UUID
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
    created_at: datetime
    updated_at: datetime
    employee_id: UUID | None = None
    internal_notes: str | None = None
