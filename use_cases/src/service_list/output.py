from dataclasses import dataclass
from datetime import date
from uuid import UUID

from domain.src.entities.service import ServiceStatus, ServiceType


@dataclass
class ServiceListItemOutput:
    id: UUID
    date: date
    customer_name: str
    service_type: ServiceType
    employee_names: list[str]
    worked_hours: float
    charged_price: float
    total_cost: float
    margin: float
    status: ServiceStatus


@dataclass
class ServiceListOutput:
    services: list[ServiceListItemOutput]
