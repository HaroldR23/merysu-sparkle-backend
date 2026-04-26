from abc import ABC, abstractmethod

from domain.src.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        """Return the user with the given email, or None if not found."""
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        """Persist a new user and return it with the assigned id."""
        pass
