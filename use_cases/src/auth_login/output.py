from dataclasses import dataclass
from uuid import UUID


@dataclass
class AuthLoginOutput:
    access_token: str
    user_id: UUID | None
    name: str
    role: str
