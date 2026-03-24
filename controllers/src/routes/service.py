from fastapi import APIRouter, Depends

from controllers.src.dependencies.service_dependencies import get_service_creation_use_case
from controllers.src.dtos.service import ServiceCreateDTO, ServiceCreateResponseDTO
from use_cases.src.service_creation.input import ServiceCreationInput
from use_cases.src.service_creation.use_case import ServiceCreationUseCase

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
            employee_id=service_dto.employee_id,
            address=service_dto.address,
            service_type=service_dto.service_type,
            distance_km=service_dto.distance_km,
            worked_hours=service_dto.worked_hours,
            hourly_rate=service_dto.hourly_rate,
            total_cost=service_dto.total_cost,
            charged_price=service_dto.charged_price,
            internal_notes=service_dto.internal_notes,
        )
    )

    return ServiceCreateResponseDTO(
        id=service.id,
        date=service.date,
        start_time=service.start_time,
        end_time=service.end_time,
        customer_id=service.customer_id,
        employee_id=service.employee_id,
        address=service.address,
        service_type=service.service_type,
        distance_km=service.distance_km,
        worked_hours=service.worked_hours,
        hourly_rate=service.hourly_rate,
        total_cost=service.total_cost,
        charged_price=service.charged_price,
        internal_notes=service.internal_notes,
        created_at=service.created_at,
        updated_at=service.updated_at,
    )
