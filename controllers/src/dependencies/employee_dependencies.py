from fastapi import Depends
from sqlalchemy.orm import Session

from adapters.src.repositories.sql_alchemy_repository.EmployeeRepository import EmployeeRepository
from adapters.src.repositories.sql_alchemy_repository.db_config import get_db
from use_cases.src.employee_creation.use_case import EmployeeCreationUseCase


def get_employee_creation_use_case(db: Session = Depends(get_db)) -> EmployeeCreationUseCase:
    return EmployeeCreationUseCase(
        employee_repository=EmployeeRepository(session=db)
    )
