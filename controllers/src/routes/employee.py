from fastapi import APIRouter, Depends
from uuid import UUID

from controllers.src.dependencies.employee_dependencies import (
    get_employee_creation_use_case,
    get_employee_list_use_case,
    get_employee_update_use_case,
)
from controllers.src.dtos.employee import (
    EmployeeCreateDTO,
    EmployeeCreateResponseDTO,
    EmployeeListItemResponseDTO,
    EmployeeListResponseDTO,
    EmployeeSummaryResponseDTO,
    EmployeeUpdateDTO,
    EmployeeUpdateResponseDTO,
)
from use_cases.src.employee_creation.input import EmployeeCreationInput
from use_cases.src.employee_creation.use_case import EmployeeCreationUseCase
from use_cases.src.employee_list.use_case import EmployeeListUseCase
from use_cases.src.employee_update.input import EmployeeUpdateInput
from use_cases.src.employee_update.use_case import EmployeeUpdateUseCase

employee_router = APIRouter()


@employee_router.post("/employees", status_code=201, response_model=EmployeeCreateResponseDTO)
def create_employee(
    employee_dto: EmployeeCreateDTO,
    employee_creation_use_case: EmployeeCreationUseCase = Depends(get_employee_creation_use_case),
):
    employee = employee_creation_use_case(
        employee_creation_input=EmployeeCreationInput(
            name=employee_dto.name,
            entry_date=employee_dto.entry_date,
            services_count=employee_dto.services_count,
            phone_number=employee_dto.phone_number,
            worked_hours=employee_dto.worked_hours,
            employee_cost=employee_dto.employee_cost,
        )
    )

    return EmployeeCreateResponseDTO(
        id=employee.id,
        name=employee.name,
        entry_date=employee.entry_date,
        services_count=employee.services_count,
        phone_number=employee.phone_number,
        worked_hours=employee.worked_hours,
        employee_cost=employee.employee_cost,
        notes=employee.notes,
        status=employee.status,
    )


@employee_router.get("/employees", status_code=200, response_model=EmployeeListResponseDTO)
def get_employees(
    employee_list_use_case: EmployeeListUseCase = Depends(get_employee_list_use_case),
):
    result = employee_list_use_case()

    return EmployeeListResponseDTO(
        summary=EmployeeSummaryResponseDTO(
            total_employees=result.summary.total_employees,
            total_hours=result.summary.total_hours,
            total_cost=result.summary.total_cost,
            total_services=result.summary.total_services,
        ),
        employees=[
            EmployeeListItemResponseDTO(
                id=e.id,
                name=e.name,
                entry_date=e.entry_date,
                phone_number=e.phone_number,
                worked_hours=e.worked_hours,
                employee_cost=e.employee_cost,
                services_count=e.services_count,
                productivity=e.productivity,
                notes=e.notes,
                status=e.status,
            )
            for e in result.employees
        ],
    )


@employee_router.patch("/employees/{id}", status_code=200, response_model=EmployeeUpdateResponseDTO)
def update_employee(
    id: UUID,
    employee_dto: EmployeeUpdateDTO,
    employee_update_use_case: EmployeeUpdateUseCase = Depends(get_employee_update_use_case),
):
    employee = employee_update_use_case(
        employee_update_input=EmployeeUpdateInput(
            id=id,
            name=employee_dto.name,
            entry_date=employee_dto.entry_date,
            phone_number=employee_dto.phone_number,
            services_count=employee_dto.services_count,
            worked_hours=employee_dto.worked_hours,
            employee_cost=employee_dto.employee_cost,
            notes=employee_dto.notes,
            status=employee_dto.status,
        )
    )

    return EmployeeUpdateResponseDTO(
        id=employee.id,
        name=employee.name,
        entry_date=employee.entry_date,
        phone_number=employee.phone_number,
        services_count=employee.services_count,
        worked_hours=employee.worked_hours,
        employee_cost=employee.employee_cost,
        notes=employee.notes,
        status=employee.status,
    )
