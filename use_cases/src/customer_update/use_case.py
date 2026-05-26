from datetime import datetime

from domain.src.entities.customer import Customer
from domain.src.exceptions.customer_exceptions import CustomerNotFoundError, InvalidCustomerDataError
from domain.src.ports.repositories.CustomerRepository import CustomerRepository
from use_cases.src.customer_update.input import CustomerUpdateInput
from use_cases.src.customer_update.output import CustomerUpdateOutput


class CustomerUpdateUseCase:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    def __call__(self, customer_update_input: CustomerUpdateInput) -> CustomerUpdateOutput:
        existing = self.customer_repository.get_by_id(customer_update_input.id)
        if existing is None:
            raise CustomerNotFoundError(f"Customer with id '{customer_update_input.id}' not found.")

        if customer_update_input.name is not None and not customer_update_input.name.strip():
            raise InvalidCustomerDataError("Customer name must not be empty.")

        if customer_update_input.services_count is not None and customer_update_input.services_count < 0:
            raise InvalidCustomerDataError("services_count must be a non-negative number.")

        if customer_update_input.total_billed is not None and customer_update_input.total_billed < 0:
            raise InvalidCustomerDataError("total_billed must be a non-negative number.")

        updated = Customer(
            id=existing.id,
            name=customer_update_input.name if customer_update_input.name is not None else existing.name,
            type=customer_update_input.type if customer_update_input.type is not None else existing.type,
            status=customer_update_input.status if customer_update_input.status is not None else existing.status,
            services_count=customer_update_input.services_count if customer_update_input.services_count is not None else existing.services_count,
            total_billed=customer_update_input.total_billed if customer_update_input.total_billed is not None else existing.total_billed,
            last_service_date=customer_update_input.last_service_date if customer_update_input.last_service_date is not None else existing.last_service_date,
            email=customer_update_input.email if customer_update_input.email is not None else existing.email,
            phone_number=customer_update_input.phone_number if customer_update_input.phone_number is not None else existing.phone_number,
            location=customer_update_input.location if customer_update_input.location is not None else existing.location,
            city=customer_update_input.city if customer_update_input.city is not None else existing.city,
            notes=customer_update_input.notes if customer_update_input.notes is not None else existing.notes,
            created_at=existing.created_at,
            updated_at=existing.updated_at,
        )

        result = self.customer_repository.update(updated)

        return CustomerUpdateOutput(
            id=result.id,  # type: ignore[arg-type]
            name=result.name,
            type=result.type,
            services_count=result.services_count,
            total_billed=result.total_billed,
            last_service_date=result.last_service_date,
            email=result.email,
            phone_number=result.phone_number,
            location=result.location,
            city=result.city,
            notes=result.notes,
            status=result.status,
            created_at=result.created_at or datetime.now(),
            updated_at=result.updated_at or datetime.now(),
        )
