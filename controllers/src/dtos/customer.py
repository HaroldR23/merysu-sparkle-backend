from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from domain.src.entities.customer import CustomerStatus, CustomerType


class CustomerCreateDTO(BaseModel):
    name: str
    type: CustomerType
    services_count: int = Field(ge=0)
    total_billed: float = Field(ge=0)
    status: CustomerStatus
    last_service_date: datetime | None = None
    email: str | None = None
    phone_number: str | None = None
    location: str | None = None
    city: str | None = None
    notes: str | None = None

    @field_validator("name")
    @classmethod
    def must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Field must not be blank.")
        return value


class CustomerCreateResponseDTO(BaseModel):
    id: UUID
    name: str
    type: CustomerType
    services_count: int
    total_billed: float
    status: CustomerStatus
    last_service_date: datetime | None
    email: str | None
    phone_number: str | None
    location: str | None
    city: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime


class CustomerSummaryResponseDTO(BaseModel):
    total_clients: int
    total_billing: float
    total_services: int
    average_billing_per_client: float


class CustomerListItemResponseDTO(BaseModel):
    id: UUID
    name: str
    type: CustomerType
    services_count: int
    total_billed: float
    status: CustomerStatus
    last_service_date: datetime | None
    email: str | None
    phone_number: str | None
    location: str | None
    city: str | None
    notes: str | None


class CustomerListResponseDTO(BaseModel):
    summary: CustomerSummaryResponseDTO
    customers: list[CustomerListItemResponseDTO]
