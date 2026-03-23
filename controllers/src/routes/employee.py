from fastapi import APIRouter, Depends

from controllers.src.dependencies.employee_dependencies import get_employee_creation_use_case
from controllers.src.dtos.employee import EmployeeCreateDTO, EmployeeCreateResponseDTO
from use_cases.src.employee_creation.input import EmployeeCreationInput
from use_cases.src.employee_creation.use_case import EmployeeCreationUseCase

employee_router = APIRouter()


@employee_router.post("/employees", status_code=201, response_model=EmployeeCreateResponseDTO)
def create_employee(
    employee_dto: EmployeeCreateDTO,
    employee_creation_use_case: EmployeeCreationUseCase = Depends(get_employee_creation_use_case),
):
    employee = employee_creation_use_case(
        employee_creation_input=EmployeeCreationInput(
            name=employee_dto.name,
            services_count=employee_dto.services_count,
            phone_number=employee_dto.phone_number,
            worked_hours=employee_dto.worked_hours,
            employee_cost=employee_dto.employee_cost,
        )
    )

    return EmployeeCreateResponseDTO(
        id=employee.id,
        name=employee.name,
        services_count=employee.services_count,
        phone_number=employee.phone_number,
        worked_hours=employee.worked_hours,
        employee_cost=employee.employee_cost,
    )
