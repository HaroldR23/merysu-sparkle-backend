from pydantic import BaseModel, Field, field_validator
from uuid import UUID


class EmployeeCreateDTO(BaseModel):
    name: str
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
    services_count: int
    phone_number: str
    worked_hours: float
    employee_cost: float


class EmployeeSummaryResponseDTO(BaseModel):
    total_employees: int
    total_hours: float
    total_cost: float
    total_services: int


class EmployeeListItemResponseDTO(BaseModel):
    id: UUID
    name: str
    worked_hours: float
    employee_cost: float
    services_count: int


class EmployeeListResponseDTO(BaseModel):
    summary: EmployeeSummaryResponseDTO
    employees: list[EmployeeListItemResponseDTO]
