from datetime import datetime, time, timezone
from typing import cast
from uuid import UUID

from domain.src.entities.service import Service
from domain.src.exceptions.customer_exceptions import CustomerNotFoundError
from domain.src.exceptions.employee_exceptions import EmployeeNotFoundError
from domain.src.exceptions.service_exceptions import InvalidServiceDataError, ServiceNotFoundError
from domain.src.ports.repositories.CustomerRepository import CustomerRepository
from domain.src.ports.repositories.EmployeeRepository import EmployeeRepository
from domain.src.ports.repositories.ServiceRepository import ServiceRepository
from use_cases.src.service_update.input import ServiceUpdateInput
from use_cases.src.service_update.output import ServiceUpdateOutput


class ServiceUpdateUseCase:
    def __init__(
        self,
        service_repository: ServiceRepository,
        customer_repository: CustomerRepository,
        employee_repository: EmployeeRepository,
    ):
        self.service_repository = service_repository
        self.customer_repository = customer_repository
        self.employee_repository = employee_repository

    def __call__(self, service_update_input: ServiceUpdateInput) -> ServiceUpdateOutput:
        existing = self.service_repository.get_by_id(service_update_input.id)
        if existing is None:
            raise ServiceNotFoundError(f"Service with id '{service_update_input.id}' not found.")

        # Build the updated service by merging patch fields over existing values
        new_date = service_update_input.date if service_update_input.date is not None else existing.date
        new_start_time = service_update_input.start_time if service_update_input.start_time is not None else existing.start_time
        new_end_time = service_update_input.end_time if service_update_input.end_time is not None else existing.end_time
        new_customer_id = service_update_input.customer_id if service_update_input.customer_id is not None else existing.customer_id
        new_address = service_update_input.address if service_update_input.address is not None else existing.address
        new_service_type = service_update_input.service_type if service_update_input.service_type is not None else existing.service_type
        new_distance_km = service_update_input.distance_km if service_update_input.distance_km is not None else existing.distance_km
        new_worked_hours = service_update_input.worked_hours if service_update_input.worked_hours is not None else existing.worked_hours
        new_hourly_rate = service_update_input.hourly_rate if service_update_input.hourly_rate is not None else existing.hourly_rate
        new_total_cost = service_update_input.total_cost if service_update_input.total_cost is not None else existing.total_cost
        new_charged_price = service_update_input.charged_price if service_update_input.charged_price is not None else existing.charged_price
        new_status = service_update_input.status if service_update_input.status is not None else existing.status
        new_employee_ids = service_update_input.employee_ids if service_update_input.employee_ids is not None else existing.employee_ids
        new_internal_notes = service_update_input.internal_notes if service_update_input.internal_notes is not None else existing.internal_notes

        # Validate merged values
        if not new_address.strip():
            raise InvalidServiceDataError("Address must not be empty.")

        if new_end_time <= new_start_time:
            raise InvalidServiceDataError("end_time must be after start_time.")

        for field_name, value in [
            ("distance_km", new_distance_km),
            ("worked_hours", new_worked_hours),
            ("hourly_rate", new_hourly_rate),
            ("total_cost", new_total_cost),
            ("charged_price", new_charged_price),
        ]:
            if value < 0:
                raise InvalidServiceDataError(f"{field_name} must be a non-negative number.")

        if self.customer_repository.get_by_id(new_customer_id) is None:
            raise CustomerNotFoundError(f"Customer with id '{new_customer_id}' not found.")

        for employee_id in new_employee_ids:
            if self.employee_repository.get_by_id(employee_id) is None:
                raise EmployeeNotFoundError(f"Employee with id '{employee_id}' not found.")

        updated_service = Service(
            id=existing.id,
            date=new_date,
            start_time=new_start_time,
            end_time=new_end_time,
            customer_id=new_customer_id,
            employee_ids=new_employee_ids,
            address=new_address,
            service_type=new_service_type,
            distance_km=new_distance_km,
            worked_hours=new_worked_hours,
            hourly_rate=new_hourly_rate,
            total_cost=new_total_cost,
            charged_price=new_charged_price,
            status=new_status,
            internal_notes=new_internal_notes,
        )

        saved = self.service_repository.update(updated_service)

        # --- Recalculate stats ---
        old_employee_ids_set = set(existing.employee_ids)
        new_employee_ids_set = set(new_employee_ids)
        old_count = len(existing.employee_ids)
        new_count = len(new_employee_ids)
        old_cost_per_emp = existing.total_cost / old_count if old_count > 0 else 0.0
        new_cost_per_emp = saved.total_cost / new_count if new_count > 0 else 0.0

        new_date_as_datetime = datetime.combine(saved.date, time.min, tzinfo=timezone.utc)

        # Customer stats
        if existing.customer_id == new_customer_id:
            self.customer_repository.update_stats(
                id=new_customer_id,
                services_count_delta=0,
                total_billed_delta=saved.charged_price - existing.charged_price,
                last_service_date=new_date_as_datetime,
            )
        else:
            old_date_as_datetime = datetime.combine(existing.date, time.min, tzinfo=timezone.utc)
            self.customer_repository.update_stats(
                id=existing.customer_id,
                services_count_delta=-1,
                total_billed_delta=-existing.charged_price,
                last_service_date=old_date_as_datetime,
            )
            self.customer_repository.update_stats(
                id=new_customer_id,
                services_count_delta=1,
                total_billed_delta=saved.charged_price,
                last_service_date=new_date_as_datetime,
            )

        # Employee stats
        removed_ids = old_employee_ids_set - new_employee_ids_set
        added_ids = new_employee_ids_set - old_employee_ids_set
        kept_ids = old_employee_ids_set & new_employee_ids_set

        for emp_id in removed_ids:
            self.employee_repository.update_stats(
                id=emp_id,
                services_count_delta=-1,
                worked_hours_delta=-existing.worked_hours,
                employee_cost_delta=-old_cost_per_emp,
            )

        for emp_id in added_ids:
            self.employee_repository.update_stats(
                id=emp_id,
                services_count_delta=1,
                worked_hours_delta=saved.worked_hours,
                employee_cost_delta=new_cost_per_emp,
            )

        old_hours_per_emp = existing.worked_hours / old_count if old_count > 0 else 0.0
        new_hours_per_emp = saved.worked_hours / new_count if new_count > 0 else 0.0
        for emp_id in kept_ids:
            self.employee_repository.update_stats(
                id=emp_id,
                services_count_delta=0,
                worked_hours_delta=new_hours_per_emp - old_hours_per_emp,
                employee_cost_delta=new_cost_per_emp - old_cost_per_emp,
            )

        margin = (
            round((saved.charged_price - saved.total_cost) / saved.charged_price * 100, 1)
            if saved.charged_price > 0
            else 0.0
        )

        return ServiceUpdateOutput(
            id=cast(UUID, saved.id),
            date=saved.date,
            start_time=saved.start_time,
            end_time=saved.end_time,
            customer_id=saved.customer_id,
            employee_ids=saved.employee_ids,
            address=saved.address,
            service_type=saved.service_type,
            distance_km=saved.distance_km,
            worked_hours=saved.worked_hours,
            hourly_rate=saved.hourly_rate,
            total_cost=saved.total_cost,
            charged_price=saved.charged_price,
            margin=margin,
            status=saved.status,
            internal_notes=saved.internal_notes,
            created_at=saved.created_at or datetime.now(timezone.utc),
            updated_at=saved.updated_at or datetime.now(timezone.utc),
        )
