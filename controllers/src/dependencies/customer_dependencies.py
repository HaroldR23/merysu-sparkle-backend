from fastapi import Depends
from sqlalchemy.orm import Session

from adapters.src.repositories.sql_alchemy_repository.CustomerRepository import CustomerRepositoryAdapter
from adapters.src.repositories.sql_alchemy_repository.db_config import get_db
from use_cases.src.customer_creation.use_case import CustomerCreationUseCase
from use_cases.src.customer_list.use_case import CustomerListUseCase
from use_cases.src.customer_update.use_case import CustomerUpdateUseCase


def get_customer_creation_use_case(db: Session = Depends(get_db)) -> CustomerCreationUseCase:
    return CustomerCreationUseCase(
        customer_repository=CustomerRepositoryAdapter(session=db)
    )


def get_customer_list_use_case(db: Session = Depends(get_db)) -> CustomerListUseCase:
    return CustomerListUseCase(
        customer_repository=CustomerRepositoryAdapter(session=db)
    )


def get_customer_update_use_case(db: Session = Depends(get_db)) -> CustomerUpdateUseCase:
    return CustomerUpdateUseCase(
        customer_repository=CustomerRepositoryAdapter(session=db)
    )
