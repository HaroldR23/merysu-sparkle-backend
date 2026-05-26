from typing import cast
from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from adapters.src.models.CustomerModel import CustomerModel
from domain.src.entities.customer import Customer, CustomerStatus, CustomerSummary, CustomerType
from domain.src.exceptions.customer_exceptions import CustomerCreationError, CustomerNotFoundError, CustomerUpdateError
from domain.src.ports.repositories.CustomerRepository import CustomerRepository





class CustomerRepositoryAdapter(CustomerRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, db_customer: CustomerModel) -> Customer:
        return Customer(
            id=cast(UUID, db_customer.id),
            name=db_customer.name,
            type=CustomerType(db_customer.type),
            services_count=db_customer.services_count,
            total_billed=db_customer.total_billed,
            last_service_date=db_customer.last_service_date,
            email=db_customer.email,
            phone_number=db_customer.phone_number,
            location=db_customer.location,
            city=db_customer.city,
            notes=db_customer.notes,
            status=CustomerStatus(db_customer.status),
            created_at=db_customer.created_at,
            updated_at=db_customer.updated_at,
        )

    def create(self, customer: Customer) -> Customer:
        db_customer = CustomerModel(
            name=customer.name,
            type=customer.type.value,
            services_count=customer.services_count,
            total_billed=customer.total_billed,
            last_service_date=customer.last_service_date,
            email=customer.email,
            phone_number=customer.phone_number,
            location=customer.location,
            city=customer.city,
            notes=customer.notes,
            status=customer.status.value,
        )
        try:
            self.session.add(db_customer)
            self.session.commit()
            self.session.refresh(db_customer)
        except Exception as e:
            self.session.rollback()
            raise CustomerCreationError() from e

        return self._to_domain(db_customer)

    def get_by_id(self, id: UUID) -> Customer | None:
        db_customer = self.session.get(CustomerModel, id)
        if db_customer is None:
            return None
        return self._to_domain(db_customer)

    def get_all_with_summary(
        self,
        status: CustomerStatus | None,
        type: CustomerType | None,
        search: str | None,
        offset: int,
        limit: int,
    ) -> tuple[list[Customer], CustomerSummary]:
        # --- Global aggregate (no filters) ---
        agg = self.session.execute(
            select(
                func.count(CustomerModel.id),
                func.coalesce(func.sum(CustomerModel.total_billed), 0.0),
                func.coalesce(func.sum(CustomerModel.services_count), 0),
            )
        ).one()

        total_clients: int = agg[0]
        total_billing: float = float(agg[1])
        total_services: int = int(agg[2])
        average_billing = total_billing / total_clients if total_clients > 0 else 0.0

        summary = CustomerSummary(
            total_clients=total_clients,
            total_billing=total_billing,
            total_services=total_services,
            average_billing_per_client=average_billing,
        )

        # --- Filtered + paginated query ---
        stmt = select(CustomerModel)

        if status is not None:
            stmt = stmt.where(CustomerModel.status == status.value)
        if type is not None:
            stmt = stmt.where(CustomerModel.type == type.value)
        if search is not None and search.strip():
            stmt = stmt.where(CustomerModel.name.ilike(f"%{search.strip()}%"))

        stmt = stmt.offset(offset).limit(limit)

        db_customers = self.session.scalars(stmt).all()

        return [self._to_domain(c) for c in db_customers], summary

    def update_stats(
        self,
        id: UUID,
        services_count_delta: int,
        total_billed_delta: float,
        last_service_date: datetime,
    ) -> None:
        db_customer = self.session.get(CustomerModel, id)
        if db_customer is None:
            raise CustomerNotFoundError(f"Customer with id '{id}' not found.")

        db_customer.services_count += services_count_delta
        db_customer.total_billed += total_billed_delta

        current = db_customer.last_service_date
        if current is None or last_service_date > current:
            db_customer.last_service_date = last_service_date

        self.session.commit()

    def update(self, customer: Customer) -> Customer:
        db_customer = self.session.get(CustomerModel, customer.id)
        if db_customer is None:
            raise CustomerNotFoundError(f"Customer with id '{customer.id}' not found.")

        db_customer.name = customer.name
        db_customer.type = customer.type.value
        db_customer.status = customer.status.value
        db_customer.services_count = customer.services_count
        db_customer.total_billed = customer.total_billed
        db_customer.last_service_date = customer.last_service_date
        db_customer.email = customer.email
        db_customer.phone_number = customer.phone_number
        db_customer.location = customer.location
        db_customer.city = customer.city
        db_customer.notes = customer.notes

        try:
            self.session.commit()
            self.session.refresh(db_customer)
        except Exception as e:
            self.session.rollback()
            raise CustomerUpdateError() from e

        return self._to_domain(db_customer)
