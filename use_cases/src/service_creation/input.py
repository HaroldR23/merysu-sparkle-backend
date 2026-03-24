from dataclasses import dataclass
from datetime import date, time
from uuid import UUID

from domain.src.entities.service import ServiceType


@dataclass
class ServiceCreationInput:
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
