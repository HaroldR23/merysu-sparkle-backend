from typing import cast
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from adapters.src.models.CustomerModel import CustomerModel
from domain.src.entities.customer import Customer, CustomerStatus, CustomerSummary, CustomerType
from domain.src.exceptions.customer_exceptions import CustomerCreationError
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
