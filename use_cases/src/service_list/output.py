from dataclasses import dataclass
from datetime import date, time
from uuid import UUID

from domain.src.entities.service import ServiceStatus, ServiceType


@dataclass
class ServiceListItemOutput:
    id: UUID
    date: date
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


@dataclass
class ServiceListOutput:
    services: list[ServiceListItemOutput]
