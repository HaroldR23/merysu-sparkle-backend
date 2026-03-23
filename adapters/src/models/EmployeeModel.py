from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4

from .Base import Base


class EmployeeModel(Base):
    __tablename__ = "employees"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    services_count: Mapped[int] = mapped_column(Integer, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    worked_hours: Mapped[float] = mapped_column(Float, nullable=False)
    employee_cost: Mapped[float] = mapped_column(Float, nullable=False)
