from typing import cast
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from adapters.src.models.EmployeeModel import EmployeeModel
from domain.src.entities.employee import Employee, EmployeeSummary
from domain.src.exceptions.employee_exceptions import EmployeeCreationError, EmployeeNotFoundError
from domain.src.ports.repositories.EmployeeRepository import EmployeeRepository

class EmployeeRepositoryAdapter(EmployeeRepository):
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

    def get_by_id(self, id: UUID) -> Employee | None:
        db_employee = self.session.get(EmployeeModel, id)
        if db_employee is None:
            return None
        return self._to_domain(db_employee)

    def get_all_with_summary(self) -> tuple[list[Employee], EmployeeSummary]:
        db_employees = self.session.scalars(select(EmployeeModel)).all()

        agg = self.session.execute(
            select(
                func.count(EmployeeModel.id),
                func.coalesce(func.sum(EmployeeModel.worked_hours), 0.0),
                func.coalesce(func.sum(EmployeeModel.employee_cost), 0.0),
                func.coalesce(func.sum(EmployeeModel.services_count), 0),
            )
        ).one()

        summary = EmployeeSummary(
            total_employees=agg[0],
            total_hours=float(agg[1]),
            total_cost=float(agg[2]),
            total_services=int(agg[3]),
        )

        return [self._to_domain(e) for e in db_employees], summary

    def update_stats(
        self,
        id: UUID,
        services_count_delta: int,
        worked_hours_delta: float,
        employee_cost_delta: float,
    ) -> None:
        db_employee = self.session.get(EmployeeModel, id)
        if db_employee is None:
            raise EmployeeNotFoundError(f"Employee with id '{id}' not found.")

        db_employee.services_count += services_count_delta
        db_employee.worked_hours += worked_hours_delta
        db_employee.employee_cost += employee_cost_delta

        self.session.commit()
