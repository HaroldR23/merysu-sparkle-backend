from fastapi import Depends
from sqlalchemy.orm import Session

from adapters.src.repositories.sql_alchemy_repository.CustomerRepository import CustomerRepositoryAdapter
from adapters.src.repositories.sql_alchemy_repository.db_config import get_db
from use_cases.src.customer_creation.use_case import CustomerCreationUseCase


def get_customer_creation_use_case(db: Session = Depends(get_db)) -> CustomerCreationUseCase:
    return CustomerCreationUseCase(
        customer_repository=CustomerRepositoryAdapter(session=db)
    )
