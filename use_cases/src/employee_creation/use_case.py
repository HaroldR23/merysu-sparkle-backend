from domain.src.entities.employee import Employee  # used to build the domain object before persisting
from domain.src.exceptions.employee_exceptions import InvalidEmployeeDataError
from domain.src.ports.repositories.EmployeeRepository import EmployeeRepository
from use_cases.src.employee_creation.input import EmployeeCreationInput
from use_cases.src.employee_creation.output import EmployeeCreationOutput


class EmployeeCreationUseCase:
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    def __call__(self, employee_creation_input: EmployeeCreationInput) -> EmployeeCreationOutput:
        if not employee_creation_input.name.strip():
            raise InvalidEmployeeDataError("Employee name must not be empty.")

        if not employee_creation_input.phone_number.strip():
            raise InvalidEmployeeDataError("Phone number must not be empty.")

        if employee_creation_input.services_count < 0:
            raise InvalidEmployeeDataError("services_count must be a non-negative number.")

        if employee_creation_input.worked_hours < 0:
            raise InvalidEmployeeDataError("worked_hours must be a non-negative number.")

        if employee_creation_input.employee_cost < 0:
            raise InvalidEmployeeDataError("employee_cost must be a non-negative number.")

        employee = Employee(
            name=employee_creation_input.name,
            entry_date=employee_creation_input.entry_date,
            services_count=employee_creation_input.services_count,
            phone_number=employee_creation_input.phone_number,
            worked_hours=employee_creation_input.worked_hours,
            employee_cost=employee_creation_input.employee_cost,
        )

        created = self.employee_repository.create(employee)

        if created.id is None:
            raise InvalidEmployeeDataError("Employee created without an ID.")

        return EmployeeCreationOutput(
            id=created.id,
            name=created.name,
            entry_date=created.entry_date,
            services_count=created.services_count,
            phone_number=created.phone_number,
            worked_hours=created.worked_hours,
            employee_cost=created.employee_cost,
            notes=created.notes,
            status=created.status,
        )
