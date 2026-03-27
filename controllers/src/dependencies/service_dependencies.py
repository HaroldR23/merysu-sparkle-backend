from fastapi import Depends
from sqlalchemy.orm import Session

from adapters.src.repositories.sql_alchemy_repository.CustomerRepository import CustomerRepositoryAdapter
from adapters.src.repositories.sql_alchemy_repository.EmployeeRepository import EmployeeRepositoryAdapter
from adapters.src.repositories.sql_alchemy_repository.ServiceRepository import ServiceRepositoryAdapter
from adapters.src.repositories.sql_alchemy_repository.db_config import get_db
from use_cases.src.service_creation.use_case import ServiceCreationUseCase
from use_cases.src.service_list.use_case import ServiceListUseCase


def get_service_creation_use_case(db: Session = Depends(get_db)) -> ServiceCreationUseCase:
    return ServiceCreationUseCase(
        service_repository=ServiceRepositoryAdapter(session=db),
        customer_repository=CustomerRepositoryAdapter(session=db),
        employee_repository=EmployeeRepositoryAdapter(session=db),
    )


def get_service_list_use_case(db: Session = Depends(get_db)) -> ServiceListUseCase:
    return ServiceListUseCase(
        service_repository=ServiceRepositoryAdapter(session=db)
    )
