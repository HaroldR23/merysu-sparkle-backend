from datetime import date
from typing import cast
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, contains_eager, selectinload

from adapters.src.models.CustomerModel import CustomerModel
from adapters.src.models.EmployeeModel import EmployeeModel
from adapters.src.models.ServiceModel import ServiceModel
from domain.src.entities.service import Service, ServiceListItem, ServiceStatus, ServiceType
from domain.src.exceptions.service_exceptions import ServiceCreationError
from domain.src.ports.repositories.ServiceRepository import ServiceRepository


class ServiceRepositoryAdapter(ServiceRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, db_service: ServiceModel) -> Service:
        return Service(
            id=cast(UUID, db_service.id),
            date=db_service.date,
            start_time=db_service.start_time,
            end_time=db_service.end_time,
            customer_id=cast(UUID, db_service.customer_id),
            employee_ids=[cast(UUID, e.id) for e in db_service.employees],
            address=db_service.address,
            service_type=ServiceType(db_service.service_type),
            distance_km=db_service.distance_km,
            worked_hours=db_service.worked_hours,
            hourly_rate=db_service.hourly_rate,
            total_cost=db_service.total_cost,
            charged_price=db_service.charged_price,
            status=ServiceStatus(db_service.status),
            internal_notes=db_service.internal_notes,
            created_at=db_service.created_at,
            updated_at=db_service.updated_at,
        )

    def _to_list_item(self, db_service: ServiceModel) -> ServiceListItem:
        charged = db_service.charged_price
        cost = db_service.total_cost
        margin = round((charged - cost) / charged * 100, 1) if charged > 0 else 0.0
        return ServiceListItem(
            id=cast(UUID, db_service.id),
            date=db_service.date,
            customer_name=db_service.customer.name,
            service_type=ServiceType(db_service.service_type),
            employee_names=[e.name for e in db_service.employees],
            worked_hours=db_service.worked_hours,
            charged_price=db_service.charged_price,
            total_cost=db_service.total_cost,
            margin=margin,
            status=ServiceStatus(db_service.status),
        )

    def create(self, service: Service) -> Service:
        db_employees: list[EmployeeModel] = []
        if service.employee_ids:
            db_employees = list(
                self.session.scalars(
                    select(EmployeeModel).where(EmployeeModel.id.in_(service.employee_ids))
                ).all()
            )

        db_service = ServiceModel(
            date=service.date,
            start_time=service.start_time,
            end_time=service.end_time,
            customer_id=service.customer_id,
            address=service.address,
            service_type=service.service_type.value,
            distance_km=service.distance_km,
            worked_hours=service.worked_hours,
            hourly_rate=service.hourly_rate,
            total_cost=service.total_cost,
            charged_price=service.charged_price,
            status=service.status.value,
            internal_notes=service.internal_notes,
            employees=db_employees,
        )
        try:
            self.session.add(db_service)
            self.session.commit()
            self.session.refresh(db_service)
        except Exception as e:
            self.session.rollback()
            raise ServiceCreationError() from e

        return self._to_domain(db_service)

    def get_all(
        self,
        search: str | None,
        date_from: date | None,
        date_to: date | None,
        offset: int,
        limit: int,
    ) -> list[ServiceListItem]:
        stmt = (
            select(ServiceModel)
            .join(ServiceModel.customer)
            .options(
                contains_eager(ServiceModel.customer),
                selectinload(ServiceModel.employees),
            )
            .order_by(ServiceModel.date.desc())
        )

        if search is not None and search.strip():
            term = f"%{search.strip()}%"
            stmt = stmt.where(
                or_(
                    CustomerModel.name.ilike(term),
                    ServiceModel.service_type.ilike(term),
                )
            )

        if date_from is not None:
            stmt = stmt.where(ServiceModel.date >= date_from)

        if date_to is not None:
            stmt = stmt.where(ServiceModel.date <= date_to)

        stmt = stmt.offset(offset).limit(limit)

        db_services = self.session.scalars(stmt).unique().all()
        return [self._to_list_item(s) for s in db_services]

