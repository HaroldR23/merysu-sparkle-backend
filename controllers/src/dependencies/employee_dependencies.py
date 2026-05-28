from fastapi import Depends
from sqlalchemy.orm import Session

from adapters.src.repositories.sql_alchemy_repository.EmployeeRepository import EmployeeRepositoryAdapter
from adapters.src.repositories.sql_alchemy_repository.db_config import get_db
from use_cases.src.employee_creation.use_case import EmployeeCreationUseCase
from use_cases.src.employee_list.use_case import EmployeeListUseCase
from use_cases.src.employee_update.use_case import EmployeeUpdateUseCase


def get_employee_creation_use_case(db: Session = Depends(get_db)) -> EmployeeCreationUseCase:
    return EmployeeCreationUseCase(
        employee_repository=EmployeeRepositoryAdapter(session=db)
    )


def get_employee_list_use_case(db: Session = Depends(get_db)) -> EmployeeListUseCase:
    return EmployeeListUseCase(
        employee_repository=EmployeeRepositoryAdapter(session=db)
    )


def get_employee_update_use_case(db: Session = Depends(get_db)) -> EmployeeUpdateUseCase:
    return EmployeeUpdateUseCase(
        employee_repository=EmployeeRepositoryAdapter(session=db)
    )
