from fastapi import APIRouter, Depends, Query
from uuid import UUID

from controllers.src.dependencies.customer_dependencies import (
    get_customer_creation_use_case,
    get_customer_list_use_case,
    get_customer_update_use_case,
)
from controllers.src.dtos.customer import (
    CustomerCreateDTO,
    CustomerCreateResponseDTO,
    CustomerListItemResponseDTO,
    CustomerListResponseDTO,
    CustomerSummaryResponseDTO,
    CustomerUpdateDTO,
    CustomerUpdateResponseDTO,
)
from domain.src.entities.customer import CustomerStatus, CustomerType
from use_cases.src.customer_creation.input import CustomerCreationInput
from use_cases.src.customer_creation.use_case import CustomerCreationUseCase
from use_cases.src.customer_list.input import CustomerListInput
from use_cases.src.customer_list.use_case import CustomerListUseCase
from use_cases.src.customer_update.input import CustomerUpdateInput
from use_cases.src.customer_update.use_case import CustomerUpdateUseCase

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
            email=customer_dto.email,
            phone_number=customer_dto.phone_number,
            location=customer_dto.location,
            city=customer_dto.city,
            notes=customer_dto.notes,
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
        email=customer.email,
        phone_number=customer.phone_number,
        location=customer.location,
        city=customer.city,
        notes=customer.notes,
        status=customer.status,
        created_at=customer.created_at,
        updated_at=customer.updated_at,
    )


@customer_router.get("/customers", status_code=200, response_model=CustomerListResponseDTO)
def get_customers(
    status: CustomerStatus | None = Query(default=None),
    type: CustomerType | None = Query(default=None),
    search: str | None = Query(default=None, max_length=100),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    customer_list_use_case: CustomerListUseCase = Depends(get_customer_list_use_case),
):
    result = customer_list_use_case(
        customer_list_input=CustomerListInput(
            status=status,
            type=type,
            search=search,
            page=page,
            page_size=page_size,
        )
    )

    return CustomerListResponseDTO(
        summary=CustomerSummaryResponseDTO(
            total_clients=result.summary.total_clients,
            total_billing=result.summary.total_billing,
            total_services=result.summary.total_services,
            average_billing_per_client=result.summary.average_billing_per_client,
        ),
        customers=[
            CustomerListItemResponseDTO(
                id=c.id,
                name=c.name,
                type=c.type,
                services_count=c.services_count,
                total_billed=c.total_billed,
                status=c.status,
                last_service_date=c.last_service_date,
                email=c.email,
                phone_number=c.phone_number,
                location=c.location,
                city=c.city,
                notes=c.notes,
            )
            for c in result.customers
        ],
    )


@customer_router.patch("/customers/{id}", status_code=200, response_model=CustomerUpdateResponseDTO)
def update_customer(
    id: UUID,
    customer_dto: CustomerUpdateDTO,
    customer_update_use_case: CustomerUpdateUseCase = Depends(get_customer_update_use_case),
):
    customer = customer_update_use_case(
        customer_update_input=CustomerUpdateInput(
            id=id,
            name=customer_dto.name,
            type=customer_dto.type,
            status=customer_dto.status,
            services_count=customer_dto.services_count,
            total_billed=customer_dto.total_billed,
            last_service_date=customer_dto.last_service_date,
            email=customer_dto.email,
            phone_number=customer_dto.phone_number,
            location=customer_dto.location,
            city=customer_dto.city,
            notes=customer_dto.notes,
        )
    )

    return CustomerUpdateResponseDTO(
        id=customer.id,
        name=customer.name,
        type=customer.type,
        services_count=customer.services_count,
        total_billed=customer.total_billed,
        last_service_date=customer.last_service_date,
        email=customer.email,
        phone_number=customer.phone_number,
        location=customer.location,
        city=customer.city,
        notes=customer.notes,
        status=customer.status,
        created_at=customer.created_at,
        updated_at=customer.updated_at,
    )
