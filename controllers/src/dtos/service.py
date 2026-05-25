from datetime import date, datetime, time
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from domain.src.entities.service import ServiceStatus, ServiceType


class ServiceCreateDTO(BaseModel):
    date: date
    start_time: time
    end_time: time
    customer_id: UUID
    address: str
    service_type: ServiceType
    distance_km: float = Field(ge=0)
    worked_hours: float = Field(ge=0)
    hourly_rate: float = Field(ge=0)
    total_cost: float = Field(ge=0)
    charged_price: float = Field(ge=0)
    status: ServiceStatus
    employee_ids: list[UUID] = Field(default_factory=list)
    internal_notes: str | None = None

    @field_validator("address")
    @classmethod
    def must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Field must not be blank.")
        return value


class ServicePatchDTO(BaseModel):
    date: datetime | None = None
    start_time: time | None = None
    end_time: time | None = None
    customer_id: UUID | None = None
    address: str | None = None
    service_type: ServiceType | None = None
    distance_km: float | None = Field(default=None, ge=0)
    worked_hours: float | None = Field(default=None, ge=0)
    hourly_rate: float | None = Field(default=None, ge=0)
    total_cost: float | None = Field(default=None, ge=0)
    charged_price: float | None = Field(default=None, ge=0)
    status: ServiceStatus | None = None
    employee_ids: list[UUID] | None = None
    internal_notes: str | None = None

    @field_validator("address")
    @classmethod
    def must_not_be_blank(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("Field must not be blank.")
        return value


class ServiceCreateResponseDTO(BaseModel):
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
    margin: float
    status: ServiceStatus
    created_at: datetime
    updated_at: datetime
    employee_ids: list[UUID]
    internal_notes: str | None


class ServiceUpdateResponseDTO(BaseModel):
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
    margin: float
    status: ServiceStatus
    created_at: datetime
    updated_at: datetime
    employee_ids: list[UUID]
    internal_notes: str | None


class ServiceListItemResponseDTO(BaseModel):
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
    internal_notes: str | None


class ServiceListResponseDTO(BaseModel):
    services: list[ServiceListItemResponseDTO]
