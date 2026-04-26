from datetime import datetime, timedelta, timezone

import jwt

from domain.src.entities.user import User
from domain.src.ports.services.JWTService import JWTService
from settings.env_variables import JWT_SECRET

_ALGORITHM = "HS256"
_EXPIRY_DAYS = 7


class JWTAdapter(JWTService):
    def create_token(self, user: User) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user.id),
            "name": user.name,
            "role": user.role.value,
            "exp": now + timedelta(days=_EXPIRY_DAYS),
            "iat": now,
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=_ALGORITHM)
