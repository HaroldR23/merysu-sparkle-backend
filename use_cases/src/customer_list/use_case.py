from typing import cast
from uuid import UUID

from domain.src.ports.repositories.CustomerRepository import CustomerRepository
from use_cases.src.customer_list.input import CustomerListInput
from use_cases.src.customer_list.output import (
    CustomerListItemOutput,
    CustomerListOutput,
    CustomerSummaryOutput,
)

_MAX_PAGE_SIZE = 100


class CustomerListUseCase:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    def __call__(self, customer_list_input: CustomerListInput) -> CustomerListOutput:
        page_size = min(customer_list_input.page_size, _MAX_PAGE_SIZE)
        offset = (customer_list_input.page - 1) * page_size

        customers, summary = self.customer_repository.get_all_with_summary(
            status=customer_list_input.status,
            type=customer_list_input.type,
            search=customer_list_input.search,
            offset=offset,
            limit=page_size,
        )

        return CustomerListOutput(
            summary=CustomerSummaryOutput(
                total_clients=summary.total_clients,
                total_billing=summary.total_billing,
                total_services=summary.total_services,
                average_billing_per_client=summary.average_billing_per_client,
            ),
            customers=[
                CustomerListItemOutput(
                    id=cast(UUID, c.id),
                    name=c.name,
                    type=c.type,
                    services_count=c.services_count,
                    total_billed=c.total_billed,
                    status=c.status,
                    last_service_date=c.last_service_date,
                )
                for c in customers
            ],
        )
