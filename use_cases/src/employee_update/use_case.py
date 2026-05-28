from domain.src.entities.employee import Employee
from domain.src.exceptions.employee_exceptions import EmployeeNotFoundError, InvalidEmployeeDataError
from domain.src.ports.repositories.EmployeeRepository import EmployeeRepository
from use_cases.src.employee_update.input import EmployeeUpdateInput
from use_cases.src.employee_update.output import EmployeeUpdateOutput


class EmployeeUpdateUseCase:
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    def __call__(self, employee_update_input: EmployeeUpdateInput) -> EmployeeUpdateOutput:
        existing = self.employee_repository.get_by_id(employee_update_input.id)
        if existing is None:
            raise EmployeeNotFoundError(f"Employee with id '{employee_update_input.id}' not found.")

        if employee_update_input.name is not None and not employee_update_input.name.strip():
            raise InvalidEmployeeDataError("Employee name must not be empty.")

        if employee_update_input.phone_number is not None and not employee_update_input.phone_number.strip():
            raise InvalidEmployeeDataError("Phone number must not be empty.")

        if employee_update_input.services_count is not None and employee_update_input.services_count < 0:
            raise InvalidEmployeeDataError("services_count must be a non-negative number.")

        if employee_update_input.worked_hours is not None and employee_update_input.worked_hours < 0:
            raise InvalidEmployeeDataError("worked_hours must be a non-negative number.")

        if employee_update_input.employee_cost is not None and employee_update_input.employee_cost < 0:
            raise InvalidEmployeeDataError("employee_cost must be a non-negative number.")

        updated = Employee(
            id=existing.id,
            name=employee_update_input.name if employee_update_input.name is not None else existing.name,
            entry_date=employee_update_input.entry_date if employee_update_input.entry_date is not None else existing.entry_date,
            phone_number=employee_update_input.phone_number if employee_update_input.phone_number is not None else existing.phone_number,
            services_count=employee_update_input.services_count if employee_update_input.services_count is not None else existing.services_count,
            worked_hours=employee_update_input.worked_hours if employee_update_input.worked_hours is not None else existing.worked_hours,
            employee_cost=employee_update_input.employee_cost if employee_update_input.employee_cost is not None else existing.employee_cost,
            notes=employee_update_input.notes if employee_update_input.notes is not None else existing.notes,
            status=employee_update_input.status if employee_update_input.status is not None else existing.status,
        )

        result = self.employee_repository.update(updated)

        return EmployeeUpdateOutput(
            id=result.id,  # type: ignore[arg-type]
            name=result.name,
            entry_date=result.entry_date,
            phone_number=result.phone_number,
            services_count=result.services_count,
            worked_hours=result.worked_hours,
            employee_cost=result.employee_cost,
            notes=result.notes,
            status=result.status,
        )
