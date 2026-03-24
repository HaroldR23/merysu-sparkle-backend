from abc import ABC, abstractmethod

from domain.src.entities.service import Service


class ServiceRepository(ABC):
    @abstractmethod
    def create(self, service: Service) -> Service:
        """Persist a new service and return it with the assigned id."""
        pass
