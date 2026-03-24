from datetime import date, datetime, time
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from domain.src.entities.service import ServiceType


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
    employee_id: UUID | None = None
    internal_notes: str | None = None

    @field_validator("address")
    @classmethod
    def must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
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
    created_at: datetime
    updated_at: datetime
    employee_id: UUID | None
    internal_notes: str | None
