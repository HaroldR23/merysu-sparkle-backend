from sqlalchemy.orm import Session
from typing import cast
from uuid import UUID

from adapters.src.models.EmployeeModel import EmployeeModel
from domain.src.entities.employee import Employee
from domain.src.exceptions.employee_exceptions import EmployeeCreationError
from domain.src.ports.EmployeeRepositoryService import EmployeeRepositoryService


class EmployeeRepository(EmployeeRepositoryService):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, db_employee: EmployeeModel) -> Employee:
        return Employee(
            id=cast(UUID, db_employee.id),
            name=db_employee.name,
            services_count=db_employee.services_count,
            phone_number=db_employee.phone_number,
            worked_hours=db_employee.worked_hours,
            employee_cost=db_employee.employee_cost,
        )

    def create(self, employee: Employee) -> Employee:
        db_employee = EmployeeModel(
            name=employee.name,
            services_count=employee.services_count,
            phone_number=employee.phone_number,
            worked_hours=employee.worked_hours,
            employee_cost=employee.employee_cost,
        )
        try:
            self.session.add(db_employee)
            self.session.commit()
            self.session.refresh(db_employee)
        except Exception as e:
            self.session.rollback()
            raise EmployeeCreationError() from e

        return self._to_domain(db_employee)
