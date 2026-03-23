from fastapi import APIRouter, Depends

from controllers.src.dependencies.customer_dependencies import get_customer_creation_use_case
from controllers.src.dtos.customer import CustomerCreateDTO, CustomerCreateResponseDTO
from use_cases.src.customer_creation.input import CustomerCreationInput
from use_cases.src.customer_creation.use_case import CustomerCreationUseCase

customer_router = APIRouter()


@customer_router.post("/customers", status_code=201, response_model=CustomerCreateResponseDTO)
def create_customer(
    customer_dto: CustomerCreateDTO,
    customer_creation_use_case: CustomerCreationUseCase = Depends(get_customer_creation_use_case),
):
    customer = customer_creation_use_case(
        customer_creation_input=CustomerCreationInput(
            name=customer_dto.name,
            type=customer_dto.type,
            services_count=customer_dto.services_count,
            total_billed=customer_dto.total_billed,
            last_service_date=customer_dto.last_service_date,
            status=customer_dto.status,
        )
    )

    return CustomerCreateResponseDTO(
        id=customer.id,
        name=customer.name,
        type=customer.type,
        services_count=customer.services_count,
        total_billed=customer.total_billed,
        last_service_date=customer.last_service_date,
        status=customer.status,
        created_at=customer.created_at,
        updated_at=customer.updated_at,
    )
