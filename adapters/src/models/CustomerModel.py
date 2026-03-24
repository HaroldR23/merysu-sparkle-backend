from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from adapters.src.models.Base import Base

if TYPE_CHECKING:
    from adapters.src.models.ServiceModel import ServiceModel


class CustomerModel(Base):
    __tablename__ = "customers"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    services_count: Mapped[int] = mapped_column(Integer, nullable=False)
    total_billed: Mapped[float] = mapped_column(Float, nullable=False)
    last_service_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    services: Mapped[list["ServiceModel"]] = relationship("ServiceModel", back_populates="customer")
