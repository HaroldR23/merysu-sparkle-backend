from typing import cast
from uuid import UUID

from domain.src.ports.repositories.ServiceRepository import ServiceRepository
from use_cases.src.service_list.input import ServiceListInput
from use_cases.src.service_list.output import ServiceListItemOutput, ServiceListOutput

_MAX_PAGE_SIZE = 100


class ServiceListUseCase:
    def __init__(self, service_repository: ServiceRepository):
        self.service_repository = service_repository

    def __call__(self, service_list_input: ServiceListInput) -> ServiceListOutput:
        page_size = min(service_list_input.page_size, _MAX_PAGE_SIZE)
        offset = (service_list_input.page - 1) * page_size

        items = self.service_repository.get_all(
            search=service_list_input.search,
            date_from=service_list_input.date_from,
            date_to=service_list_input.date_to,
            offset=offset,
            limit=page_size,
        )

        return ServiceListOutput(
            services=[
                ServiceListItemOutput(
                    id=cast(UUID, item.id),
                    date=item.date,
                    start_time=item.start_time,
                    end_time=item.end_time,
                    customer_id=item.customer_id,
                    customer_name=item.customer_name,
                    address=item.address,
                    service_type=item.service_type,
                    distance_km=item.distance_km,
                    hourly_rate=item.hourly_rate,
                    employee_names=item.employee_names,
                    worked_hours=item.worked_hours,
                    charged_price=item.charged_price,
                    total_cost=item.total_cost,
                    margin=item.margin,
                    status=item.status,
                    internal_notes=item.internal_notes,
                )
                for item in items
            ]
        )
