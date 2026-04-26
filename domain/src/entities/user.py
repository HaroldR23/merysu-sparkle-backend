from dataclasses import dataclass
from enum import Enum
from uuid import UUID


class UserRole(str, Enum):
    admin = "admin"


@dataclass
class User:
    email: str
    name: str
    role: UserRole
    hashed_password: str
    id: UUID | None = None
