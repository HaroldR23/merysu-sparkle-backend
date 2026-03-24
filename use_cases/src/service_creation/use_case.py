from datetime import datetime

from domain.src.entities.service import Service
from domain.src.exceptions.customer_exceptions import CustomerNotFoundError
from domain.src.exceptions.employee_exceptions import EmployeeNotFoundError
from domain.src.exceptions.service_exceptions import InvalidServiceDataError
from domain.src.ports.repositories.CustomerRepository import CustomerRepository
from domain.src.ports.repositories.EmployeeRepository import EmployeeRepository
from domain.src.ports.repositories.ServiceRepository import ServiceRepository
from use_cases.src.service_creation.input import ServiceCreationInput
from use_cases.src.service_creation.output import ServiceCreationOutput


class ServiceCreationUseCase:
    def __init__(
        self,
        service_repository: ServiceRepository,
        customer_repository: CustomerRepository,
        employee_repository: EmployeeRepository,
    ):
        self.service_repository = service_repository
        self.customer_repository = customer_repository
        self.employee_repository = employee_repository

    def __call__(self, service_creation_input: ServiceCreationInput) -> ServiceCreationOutput:
        if not service_creation_input.address.strip():
            raise InvalidServiceDataError("Address must not be empty.")

        if service_creation_input.end_time <= service_creation_input.start_time:
            raise InvalidServiceDataError("end_time must be after start_time.")

        for field_name, value in [
            ("distance_km", service_creation_input.distance_km),
            ("worked_hours", service_creation_input.worked_hours),
            ("hourly_rate", service_creation_input.hourly_rate),
            ("total_cost", service_creation_input.total_cost),
            ("charged_price", service_creation_input.charged_price),
        ]:
            if value < 0:
                raise InvalidServiceDataError(f"{field_name} must be a non-negative number.")

        if self.customer_repository.get_by_id(service_creation_input.customer_id) is None:
            raise CustomerNotFoundError(f"Customer with id '{service_creation_input.customer_id}' not found.")

        if service_creation_input.employee_id is not None:
            if self.employee_repository.get_by_id(service_creation_input.employee_id) is None:
                raise EmployeeNotFoundError(f"Employee with id '{service_creation_input.employee_id}' not found.")

        service = Service(
            date=service_creation_input.date,
            start_time=service_creation_input.start_time,
            end_time=service_creation_input.end_time,
            customer_id=service_creation_input.customer_id,
            employee_id=service_creation_input.employee_id,
            address=service_creation_input.address,
            service_type=service_creation_input.service_type,
            distance_km=service_creation_input.distance_km,
            worked_hours=service_creation_input.worked_hours,
            hourly_rate=service_creation_input.hourly_rate,
            total_cost=service_creation_input.total_cost,
            charged_price=service_creation_input.charged_price,
            internal_notes=service_creation_input.internal_notes,
        )

        created = self.service_repository.create(service)

        if created.id is None:
            raise InvalidServiceDataError("Service created without an ID.")

        return ServiceCreationOutput(
            id=created.id,
            date=created.date,
            start_time=created.start_time,
            end_time=created.end_time,
            customer_id=created.customer_id,
            employee_id=created.employee_id,
            address=created.address,
            service_type=created.service_type,
            distance_km=created.distance_km,
            worked_hours=created.worked_hours,
            hourly_rate=created.hourly_rate,
            total_cost=created.total_cost,
            charged_price=created.charged_price,
            internal_notes=created.internal_notes,
            created_at=created.created_at or datetime.now(),
            updated_at=created.updated_at or datetime.now(),
        )
