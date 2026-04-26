from abc import ABC, abstractmethod

from domain.src.entities.user import User


class JWTService(ABC):
    @abstractmethod
    def create_token(self, user: User) -> str:
        """Generate and return a signed JWT for the given user."""
        pass
