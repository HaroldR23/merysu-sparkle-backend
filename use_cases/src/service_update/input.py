from dataclasses import dataclass
from datetime import datetime, time
from uuid import UUID

from domain.src.entities.service import ServiceStatus, ServiceType


@dataclass
class ServiceUpdateInput:
    id: UUID
    date: datetime | None = None
    start_time: time | None = None
    end_time: time | None = None
    customer_id: UUID | None = None
    address: str | None = None
    service_type: ServiceType | None = None
    distance_km: float | None = None
    worked_hours: float | None = None
    hourly_rate: float | None = None
    total_cost: float | None = None
    charged_price: float | None = None
    status: ServiceStatus | None = None
    employee_ids: list[UUID] | None = None
    internal_notes: str | None = None
