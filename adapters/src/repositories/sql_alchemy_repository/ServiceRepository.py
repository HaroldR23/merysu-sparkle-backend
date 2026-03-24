from typing import cast
from uuid import UUID

from sqlalchemy.orm import Session

from adapters.src.models.ServiceModel import ServiceModel
from domain.src.entities.service import Service, ServiceType
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
            employee_id=cast(UUID, db_service.employee_id) if db_service.employee_id else None,
            address=db_service.address,
            service_type=ServiceType(db_service.service_type),
            distance_km=db_service.distance_km,
            worked_hours=db_service.worked_hours,
            hourly_rate=db_service.hourly_rate,
            total_cost=db_service.total_cost,
            charged_price=db_service.charged_price,
            internal_notes=db_service.internal_notes,
            created_at=db_service.created_at,
            updated_at=db_service.updated_at,
        )

    def create(self, service: Service) -> Service:
        db_service = ServiceModel(
            date=service.date,
            start_time=service.start_time,
            end_time=service.end_time,
            customer_id=service.customer_id,
            employee_id=service.employee_id,
            address=service.address,
            service_type=service.service_type.value,
            distance_km=service.distance_km,
            worked_hours=service.worked_hours,
            hourly_rate=service.hourly_rate,
            total_cost=service.total_cost,
            charged_price=service.charged_price,
            internal_notes=service.internal_notes,
        )
        try:
            self.session.add(db_service)
            self.session.commit()
            self.session.refresh(db_service)
        except Exception as e:
            self.session.rollback()
            raise ServiceCreationError() from e

        return self._to_domain(db_service)
