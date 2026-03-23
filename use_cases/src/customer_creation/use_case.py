from datetime import datetime
from domain.src.entities.customer import Customer
from domain.src.exceptions.customer_exceptions import InvalidCustomerDataError
from domain.src.ports.repositories.CustomerRepository import CustomerRepository
from use_cases.src.customer_creation.input import CustomerCreationInput
from use_cases.src.customer_creation.output import CustomerCreationOutput


class CustomerCreationUseCase:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    def __call__(self, customer_creation_input: CustomerCreationInput) -> CustomerCreationOutput:
        if not customer_creation_input.name.strip():
            raise InvalidCustomerDataError("Customer name must not be empty.")

        if customer_creation_input.services_count < 0:
            raise InvalidCustomerDataError("services_count must be a non-negative number.")

        if customer_creation_input.total_billed < 0:
            raise InvalidCustomerDataError("total_billed must be a non-negative number.")

        customer = Customer(
            name=customer_creation_input.name,
            type=customer_creation_input.type,
            services_count=customer_creation_input.services_count,
            total_billed=customer_creation_input.total_billed,
            last_service_date=customer_creation_input.last_service_date,
            status=customer_creation_input.status,
        )

        created = self.customer_repository.create(customer)

        if created.id is None:
            raise InvalidCustomerDataError("Customer created without an ID.")

        return CustomerCreationOutput(
            id=created.id,
            name=created.name,
            type=created.type,
            services_count=created.services_count,
            total_billed=created.total_billed,
            last_service_date=created.last_service_date,
            status=created.status,
            created_at=created.created_at or datetime.now(),
            updated_at=created.updated_at  or datetime.now(),
        )
