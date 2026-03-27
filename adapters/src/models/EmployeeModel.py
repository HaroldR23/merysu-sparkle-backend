from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .Base import Base
from adapters.src.models.ServiceModel import service_employees

if TYPE_CHECKING:
    from adapters.src.models.ServiceModel import ServiceModel


class EmployeeModel(Base):
    __tablename__ = "employees"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    services_count: Mapped[int] = mapped_column(Integer, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    worked_hours: Mapped[float] = mapped_column(Float, nullable=False)
    employee_cost: Mapped[float] = mapped_column(Float, nullable=False)

    services: Mapped[list["ServiceModel"]] = relationship(
        "ServiceModel", secondary=service_employees, back_populates="employees"
    )
