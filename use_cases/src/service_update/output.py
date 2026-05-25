from dataclasses import dataclass, field
from datetime import datetime, time
from uuid import UUID

from domain.src.entities.service import ServiceStatus, ServiceType


@dataclass
class ServiceUpdateOutput:
    id: UUID
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
    margin: float
    status: ServiceStatus
    created_at: datetime
    updated_at: datetime
    employee_ids: list[UUID] = field(default_factory=list)
    internal_notes: str | None = None
