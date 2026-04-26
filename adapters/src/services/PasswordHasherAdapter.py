import bcrypt

from domain.src.ports.services.PasswordHasher import PasswordHasher

_ROUNDS = 12

# Precomputed dummy hash used to normalise timing when the user is not found,
# preventing user-enumeration via response-time differences.
_DUMMY_HASH = bcrypt.hashpw(b"dummy", bcrypt.gensalt(rounds=_ROUNDS)).decode()


class PasswordHasherAdapter(PasswordHasher):
    def hash(self, plain_password: str) -> str:
        hashed = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt(rounds=_ROUNDS))
        return hashed.decode()

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

    def dummy_verify(self, plain_password: str) -> None:
        """Run a bcrypt check against a dummy hash to normalise timing."""
        bcrypt.checkpw(plain_password.encode(), _DUMMY_HASH.encode())
