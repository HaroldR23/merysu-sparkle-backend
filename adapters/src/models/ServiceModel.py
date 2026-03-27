from __future__ import annotations

from datetime import date, datetime, time, timezone
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, String, Table, Text, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from adapters.src.models.Base import Base

if TYPE_CHECKING:
    from adapters.src.models.CustomerModel import CustomerModel
    from adapters.src.models.EmployeeModel import EmployeeModel


service_employees = Table(
    "service_employees",
    Base.metadata,
    Column("service_id", ForeignKey("services.id"), primary_key=True),
    Column("employee_id", ForeignKey("employees.id"), primary_key=True),
)


class ServiceModel(Base):
    __tablename__ = "services"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    customer_id: Mapped[UUID] = mapped_column(ForeignKey("customers.id"), nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    service_type: Mapped[str] = mapped_column(String, nullable=False)
    distance_km: Mapped[float] = mapped_column(Float, nullable=False)
    worked_hours: Mapped[float] = mapped_column(Float, nullable=False)
    hourly_rate: Mapped[float] = mapped_column(Float, nullable=False)
    total_cost: Mapped[float] = mapped_column(Float, nullable=False)
    charged_price: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    internal_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    customer: Mapped["CustomerModel"] = relationship("CustomerModel", back_populates="services")
    employees: Mapped[list["EmployeeModel"]] = relationship(
        "EmployeeModel", secondary=service_employees, back_populates="services"
    )
