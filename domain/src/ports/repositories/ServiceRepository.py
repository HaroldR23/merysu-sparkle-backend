from abc import ABC, abstractmethod
from datetime import date

from domain.src.entities.service import Service, ServiceListItem


class ServiceRepository(ABC):
    @abstractmethod
    def create(self, service: Service) -> Service:
        """Persist a new service and return it with the assigned id."""
        pass

    @abstractmethod
    def get_all(
        self,
        search: str | None,
        date_from: date | None,
        date_to: date | None,
        offset: int,
        limit: int,
    ) -> list[ServiceListItem]:
        """Return a filtered, paginated list of service list items."""
        pass
