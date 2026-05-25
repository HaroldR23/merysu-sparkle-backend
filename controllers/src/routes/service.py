from datetime import date

from fastapi import APIRouter, Depends, Query

from controllers.src.dependencies.service_dependencies import (
    get_service_creation_use_case,
    get_service_list_use_case,
)
from controllers.src.dtos.service import (
    ServiceCreateDTO,
    ServiceCreateResponseDTO,
    ServiceListItemResponseDTO,
    ServiceListResponseDTO,
)
from use_cases.src.service_creation.input import ServiceCreationInput
from use_cases.src.service_creation.use_case import ServiceCreationUseCase
from use_cases.src.service_list.input import ServiceListInput
from use_cases.src.service_list.use_case import ServiceListUseCase

service_router = APIRouter()


@service_router.post("/services", status_code=201, response_model=ServiceCreateResponseDTO)
def create_service(
    service_dto: ServiceCreateDTO,
    service_creation_use_case: ServiceCreationUseCase = Depends(get_service_creation_use_case),
):
    service = service_creation_use_case(
        service_creation_input=ServiceCreationInput(
            date=service_dto.date,
            start_time=service_dto.start_time,
            end_time=service_dto.end_time,
            customer_id=service_dto.customer_id,
            employee_ids=service_dto.employee_ids,
            address=service_dto.address,
            service_type=service_dto.service_type,
            distance_km=service_dto.distance_km,
            worked_hours=service_dto.worked_hours,
            hourly_rate=service_dto.hourly_rate,
            total_cost=service_dto.total_cost,
            charged_price=service_dto.charged_price,
            status=service_dto.status,
            internal_notes=service_dto.internal_notes,
        )
    )

    return ServiceCreateResponseDTO(
        id=service.id,
        date=service.date,
        start_time=service.start_time,
        end_time=service.end_time,
        customer_id=service.customer_id,
        employee_ids=service.employee_ids,
        address=service.address,
        service_type=service.service_type,
        distance_km=service.distance_km,
        worked_hours=service.worked_hours,
        hourly_rate=service.hourly_rate,
        total_cost=service.total_cost,
        charged_price=service.charged_price,
        margin=service.margin,
        status=service.status,
        internal_notes=service.internal_notes,
        created_at=service.created_at,
        updated_at=service.updated_at,
    )


@service_router.get("/services", status_code=200, response_model=ServiceListResponseDTO)
def get_services(
    search: str | None = Query(default=None, max_length=100),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    service_list_use_case: ServiceListUseCase = Depends(get_service_list_use_case),
):
    result = service_list_use_case(
        service_list_input=ServiceListInput(
            search=search,
            date_from=date_from,
            date_to=date_to,
            page=page,
            page_size=page_size,
        )
    )

    return ServiceListResponseDTO(
        services=[
            ServiceListItemResponseDTO(
                id=s.id,
                date=s.date,
                start_time=s.start_time,
                end_time=s.end_time,
                customer_id=s.customer_id,
                customer_name=s.customer_name,
                address=s.address,
                service_type=s.service_type,
                distance_km=s.distance_km,
                hourly_rate=s.hourly_rate,
                employee_names=s.employee_names,
                worked_hours=s.worked_hours,
                charged_price=s.charged_price,
                total_cost=s.total_cost,
                margin=s.margin,
                status=s.status,
                internal_notes=s.internal_notes,
            )
            for s in result.services
        ]
    )
