from datetime import date

from pydantic import BaseModel, Field, field_validator
from uuid import UUID

from domain.src.entities.employee import EmployeeStatus


class EmployeeCreateDTO(BaseModel):
    name: str
    entry_date: date
    services_count: int = Field(ge=0)
    phone_number: str
    worked_hours: float = Field(ge=0)
    employee_cost: float = Field(ge=0)

    @field_validator("name", "phone_number")
    @classmethod
    def must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Field must not be blank.")
        return value


class EmployeeCreateResponseDTO(BaseModel):
    id: UUID
    name: str
    entry_date: date
    services_count: int
    phone_number: str
    worked_hours: float
    employee_cost: float
    status: EmployeeStatus
    notes: str | None


class EmployeeSummaryResponseDTO(BaseModel):
    total_employees: int
    total_hours: float
    total_cost: float
    total_services: int


class EmployeeListItemResponseDTO(BaseModel):
    id: UUID
    name: str
    entry_date: date
    phone_number: str
    worked_hours: float
    employee_cost: float
    services_count: int
    productivity: float
    status: EmployeeStatus
    notes: str | None


class EmployeeListResponseDTO(BaseModel):
    summary: EmployeeSummaryResponseDTO
    employees: list[EmployeeListItemResponseDTO]


class EmployeeUpdateDTO(BaseModel):
    name: str | None = None
    entry_date: date | None = None
    phone_number: str | None = None
    services_count: int | None = Field(default=None, ge=0)
    worked_hours: float | None = Field(default=None, ge=0)
    employee_cost: float | None = Field(default=None, ge=0)
    notes: str | None = None
    status: EmployeeStatus | None = None

    @field_validator("name", "phone_number")
    @classmethod
    def must_not_be_blank(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("Field must not be blank.")
        return value


class EmployeeUpdateResponseDTO(BaseModel):
    id: UUID
    name: str
    entry_date: date
    phone_number: str
    services_count: int
    worked_hours: float
    employee_cost: float
    status: EmployeeStatus
    notes: str | None
